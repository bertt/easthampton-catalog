"""Frame and render a thumbnail for every collection with chiitiler.

Follows the portolan-thumbnails skill: strategy A frames the whole extent,
strategy B frames a zoomed window on a dense cluster. Needs a running
chiitiler server (start_server.sh) and the PMTiles files built locally.

    SKILL=<skill dir> python3 tools/make_thumbs.py [collection ...]
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
SKILL = Path(os.environ["SKILL"]) / "scripts"
WORK = Path(os.environ.get("WORK", "/tmp/portolan-thumbs"))
WORK.mkdir(parents=True, exist_ok=True)
SIZE = 1024
FORCE_B = {"building_footprints": 15, "ehtaxmap": 15, "aho_lbo": 14, "trails": 13,
           "limwa_limit_of_moderate_wave_action": 13, "scenic_conservation_easements": 14,
           "recreational_open_space": 14, "wetlands_in_east_hampton": 14,
           # Small features scattered across the town vanish at full extent.
           "fire_departments": 14, "historcal_wetlands": 14, "protected_veg_buffer_areas": 14,
           "school_properties": 14, "town_facilities": 14, "upland_areas": 14, "watercourses": 14,
           "eh_historic_districts": 14, "protected_ag_land": 13, "wetlands_not_georeferenced": 14}
# The basemap serves "Map data not yet available" tiles too deep here, so frame wider on the bbox centre.
CENTER_ZOOM = {}
# Features too small to read at any town-scale window: centre on the largest one.
LARGEST = {"fire_departments": 16, "historcal_wetlands": 15, "protected_veg_buffer_areas": 15,
           "upland_areas": 15, "recreation_overlay_district": 14}

con = duckdb.connect()
con.execute("install spatial; load spatial;")


def frame(*args):
    out = subprocess.run([sys.executable, str(SKILL / "frame.py"), *args, "--size", str(SIZE)],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def dense_center(parquet, zoom, rank):
    cell = 40075016.686 * SIZE / (256 * 2 ** zoom) / 111319.49
    rows = con.execute(f"""
      WITH c AS (
        SELECT ST_X(p) x, ST_Y(p) y FROM (
          SELECT ST_Transform(ST_Centroid(geometry), 'EPSG:2263', 'EPSG:4326', always_xy := true) p
          FROM read_parquet('{parquet}'))
      ), g AS (SELECT floor(x/{cell}) gx, floor(y/{cell}) gy, count(*) n FROM c GROUP BY 1,2
               ORDER BY n DESC LIMIT 1 OFFSET {rank})
      SELECT count(*), avg(x), avg(y) FROM c, g
      WHERE x BETWEEN (gx-1)*{cell} AND (gx+2)*{cell} AND y BETWEEN (gy-1)*{cell} AND (gy+2)*{cell}
    """).fetchone()
    return rows


def ensure_thumb_asset(cdir, cid):
    path = cdir / "collection.json"
    stac = json.loads(path.read_text())
    if not any("thumbnail" in (a.get("roles") or []) for a in stac["assets"].values()):
        stac["assets"]["thumbnail"] = {
            "href": f"./{cid}.thumb.jpg", "type": "image/jpeg", "roles": ["thumbnail"],
            "title": f"{stac['title']} thumbnail"}
        path.write_text(json.dumps(stac, indent=2) + "\n")


names = sys.argv[1:] or [p.name for p in sorted(ROOT.iterdir()) if (p / "collection.json").exists()]
log = open(WORK / "framing.tsv", "a")
b_rank = 0
for cid in names:
    cdir = ROOT / cid
    stac = json.loads((cdir / "collection.json").read_text())
    ensure_thumb_asset(cdir, cid)
    bbox = ",".join(str(v) for v in stac["extent"]["spatial"]["bbox"][0])
    a = frame("--bbox", bbox)
    strategy, zoom, rank, final = "A", a["zoom"], "-", a["bbox"]
    if cid in FORCE_B:
        strategy, zoom, rank = "B", FORCE_B[cid], b_rank % 3
    elif a["fill"] < 0.4 and stac["geoparquet:feature_count"] > 50:
        strategy, zoom, rank = "B", 14, b_rank % 3
    if cid in LARGEST:
        strategy, zoom = "B", LARGEST[cid]
        x, y = con.execute(f"""
          SELECT ST_X(p), ST_Y(p) FROM (
            SELECT ST_Transform(ST_Centroid(geometry), 'EPSG:2263', 'EPSG:4326', always_xy := true) p
            FROM read_parquet('{cdir / (cid + '.parquet')}') ORDER BY ST_Area(geometry) DESC LIMIT 1)
        """).fetchone()
        final = frame("--center", f"{x:.6f},{y:.6f}", "--zoom", str(zoom))["bbox"]
    elif cid in CENTER_ZOOM:
        strategy, zoom = "B", CENTER_ZOOM[cid]
        w, s_, e, n_ = stac["extent"]["spatial"]["bbox"][0]
        final = frame("--center", f"{(w + e) / 2:.6f},{(s_ + n_) / 2:.6f}", "--zoom", str(zoom))["bbox"]
    elif strategy == "B":
        n, x, y = dense_center(cdir / f"{cid}.parquet", zoom, rank)
        final = frame("--center", f"{x:.6f},{y:.6f}", "--zoom", str(zoom))["bbox"]
    if strategy == "B":
        b_rank += 1
    res = subprocess.run(["bash", str(SKILL / "render_one.sh"), str(cdir), final],
                         capture_output=True, text=True, env={**os.environ, "WORK": str(WORK)})
    msg = (res.stdout + res.stderr).strip().splitlines()[-1] if (res.stdout + res.stderr).strip() else ""
    print(f"{cid}\t{strategy}\t{zoom}\t{msg}", flush=True)
    log.write(f"{cid}\t{strategy}\t{final}\t{zoom}\t{rank}\tpending\n")
