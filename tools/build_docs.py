"""Generate collection and root documentation for the East Hampton mirror.

Writes AGENTS.md per collection and at the root, patches STAC title,
description and table:columns descriptions, and updates metadata.yaml notes.
Every fact is either attested by the source service's layer JSON or derived
from the mirrored data. Every SQL recipe is executed before it is written.

Run from anywhere with the portolan-cli virtualenv python (needs duckdb,
pyyaml, requests):
    python tools/build_docs.py
"""

import json
import os
import re
import subprocess
from pathlib import Path

import duckdb
import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
SERVICE = "https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer"
EXTRACTED = "2026-10-21"
NOTES = (
    f"Extracted {EXTRACTED} with portolan-cli 0.8.0 from the ArcGIS MapServer [{SERVICE}]({SERVICE}), "
    "one GeoParquet file per feature layer, in the service's native CRS (EPSG:2263). Group layers, "
    "which hold no data of their own, were skipped. Layer 81 (a duplicate of layer 56, EH Waterbodies) "
    "is not mirrored separately. The service states it exists for the Town's OpenGov application and "
    "contains draft data that may be incomplete."
)
GEOM_WORDS = {"MultiPolygon": "polygon", "Polygon": "polygon", "MultiLineString": "line",
              "LineString": "line", "Point": "point", "MultiPoint": "point"}

con = duckdb.connect()
con.execute("install spatial; load spatial;")

service = requests.get(f"{SERVICE}?f=json", timeout=60).json()
layer_names = {l["id"]: l["name"].strip() for l in service["layers"]}
parents = {l["id"]: l["parentLayerId"] for l in service["layers"]}


def q(sql):
    return con.execute(sql).fetchall()


def clean_text(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


collections = []
for cdir in sorted(p for p in ROOT.iterdir() if (p / "collection.json").exists()):
    cid = cdir.name
    stac_path = cdir / "collection.json"
    stac = json.loads(stac_path.read_text())
    meta_path = cdir / ".portolan" / "metadata.yaml"
    meta = yaml.safe_load(meta_path.read_text())
    lid = int(meta["source_url"].rstrip("/").rsplit("/", 1)[1])
    layer = requests.get(f"{SERVICE}/{lid}?f=json", timeout=60).json()
    name = layer["name"].strip()
    parent = parents.get(lid, -1)
    group = layer_names.get(parent) if parent != -1 else None
    ppath = f"{cid}/{cid}.parquet"
    n = q(f"select count(*) from read_parquet('{ppath}')")[0][0]
    gtype = stac["geoparquet:geometry_type"]
    gword = GEOM_WORDS.get(gtype, gtype)
    crs = stac["assets"][cid]["proj:code"]
    bbox = stac["extent"]["spatial"]["bbox"][0]

    pub_desc = clean_text(layer.get("description"))
    credit = clean_text(layer.get("copyrightText"))
    if pub_desc == name:
        pub_desc = ""
    fields = {f["name"]: f for f in layer["fields"]}
    has_shape = any(c["name"] == "Shape" for c in stac["table:columns"])
    shape_null = has_shape and q(f"select count(Shape) = 0 from read_parquet('{ppath}')")[0][0]
    cols = [c for c in stac["table:columns"] if c["name"] not in ("geometry", "bbox", "Shape")]

    colinfo = []
    for c in cols:
        cn = c["name"]
        f = fields.get(cn, {})
        parts = []
        alias = f.get("alias")
        if alias and alias != cn:
            parts.append(f"Alias in the source service: \"{alias}\".")
        dom = f.get("domain")
        if dom and dom.get("codedValues"):
            codes = "; ".join(f"{v['code']} = {v['name']}" for v in dom["codedValues"])
            parts.append(f"Coded values (service domain): {codes}.")
        distinct, nonnull = q(f'select count(distinct "{cn}"), count("{cn}") from read_parquet(\'{ppath}\')')[0]
        top = None
        if c["type"] == "string" and 1 <= distinct <= 12:
            top = q(f'select "{cn}", count(*) from read_parquet(\'{ppath}\') where "{cn}" is not null '
                    f'group by 1 order by 2 desc')
        colinfo.append({"name": cn, "type": c["type"], "desc": " ".join(parts), "nulls": n - nonnull,
                        "distinct": distinct, "top": top})
        if parts:
            c["description"] = " ".join(parts)

    recipes = [("Row count", f"SELECT count(*) AS features FROM read_parquet('{ppath}');")]
    cat = next((ci for ci in colinfo if ci["top"] and len(ci["top"]) >= 2 and ci["nulls"] < n), None)
    if cat:
        recipes.append((f"Features per `{cat['name']}`",
                        f'SELECT "{cat["name"]}", count(*) AS features\nFROM read_parquet(\'{ppath}\')\n'
                        f'GROUP BY 1 ORDER BY 2 DESC;'))
    if gword == "polygon":
        recipes.append(("Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet)",
                        f"SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres\n"
                        f"FROM read_parquet('{ppath}');"))
    elif gword == "line":
        recipes.append(("Total length in miles, computed from the geometry (EPSG:2263 is in US survey feet)",
                        f"SELECT round(sum(ST_Length(geometry)) / 5280, 1) AS miles\n"
                        f"FROM read_parquet('{ppath}');"))
    recipes.append(("Reproject to WGS84 for web maps",
                    f"SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326\n"
                    f"FROM read_parquet('{ppath}')\nLIMIT 5;"))
    for _, sql in recipes:
        con.execute(sql).fetchall()

    desc = (f"Mirror of the \"{name}\" layer (layer {lid}"
            + (f", in the service's \"{group}\" group" if group else "")
            + f") of the Town of East Hampton's [MapServiceForOpenGov]({SERVICE}) ArcGIS service. "
            f"{n:,} {gword} feature{'s' if n != 1 else ''}, kept in the source CRS {crs}. "
            "The service warns that it contains draft data that may be incomplete.")
    if pub_desc:
        desc += f" The publisher describes it as: \"{pub_desc}\""
    if credit:
        desc += f" Credit given by the publisher on this layer: {credit}."
    full_desc = desc + " See [AGENTS.md](AGENTS.md) for the schema, quirks and query recipes."
    stac["title"] = name
    stac["description"] = full_desc
    meta["description"] = full_desc
    stac_path.write_text(json.dumps(stac, indent=2) + "\n")

    meta["processing_notes"] = (
        f"Extracted {EXTRACTED} with portolan-cli 0.8.0 from ArcGIS MapServer layer {lid} "
        f"([{name}]({meta['source_url']})). See the root README for the full process.")
    meta_path.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=100))

    L = [f"# AGENTS.md — {name}\n",
         f"Guidance for working with the `{cid}` collection. Catalog-wide context is in the "
         "[root AGENTS.md](../AGENTS.md).\n",
         "## Overview\n", desc + "\n",
         f"- Source layer: [{name}]({meta['source_url']}) (layer id {lid}).",
         f"- Rows: {n:,}. Geometry: {gtype}. CRS: {crs} (NAD83 / New York Long Island, US survey feet).",
         f"- Bounding box (EPSG:4326): {', '.join(f'{b:.4f}' for b in bbox)}.\n",
         "## Accessing the data\n",
         "Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.\n",
         "```sql\n" + recipes[0][1] + "\n```\n",
         "## Schema & field notes\n",
         "Types come from the GeoParquet file. Alias and coded-value text is copied from the source "
         "layer's field metadata. Where the source gives no alias or code list, the column is listed "
         "without a meaning: the publisher has not documented it, and this catalog does not guess.\n",
         "| Column | Type | Meaning from the source | Nulls | Distinct |",
         "|---|---|---|---|---|"]
    for ci in colinfo:
        L.append(f"| `{ci['name']}` | {ci['type']} | {md_escape(ci['desc']) or 'Not documented by the publisher.'} "
                 f"| {ci['nulls']:,} | {ci['distinct']:,} |")
    L.append("| `geometry` | binary (WKB) | Feature geometry. | 0 | |")
    L.append("| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |")
    if shape_null:
        L.append("| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |")
    L.append("")
    cats = [ci for ci in colinfo if ci["top"]]
    if cats:
        L.append("### Observed values of low-cardinality text columns\n")
        L.append("Computed from the mirrored data, so they describe this snapshot and may differ upstream.\n")
        for ci in cats:
            L.append(f"- `{ci['name']}`: " + ", ".join(f"`{v}` ({c:,})" for v, c in ci["top"]))
        L.append("")
    L += ["## Data quality & usage notes\n",
          "- The source service says it is built for the Town's OpenGov application and \"contains draft "
          "data that may be incomplete\".",
          f"- Coordinates are in {crs}, in US survey feet. Areas and lengths computed from the geometry "
          "are in square feet and feet. Reproject to EPSG:4326 for web maps.",
          "- Geometry is stored as it came from the service. Nothing was cleaned or filtered.\n",
          "## Example queries\n"]
    for label, sql in recipes[1:]:
        L += [f"{label}:\n", "```sql\n" + sql + "\n```\n"]
    L += ["## Related collections\n",
          "The source service defines no foreign keys between layers. See the "
          "[root AGENTS.md](../AGENTS.md) for the one join this catalog documents.\n"]
    (cdir / "AGENTS.md").write_text("\n".join(L))
    collections.append((cid, name, lid, group, gtype, n))

total = sum(c[5] for c in collections)
cat_json = json.loads((ROOT / "catalog.json").read_text())
cat_json["title"] = "East Hampton, NY GIS Layers (mirror)"
cat_json["description"] = (
    f"Mirror of {len(collections)} feature layers ({total:,} features) from the Town of East Hampton, New York's "
    f"[MapServiceForOpenGov]({SERVICE}) ArcGIS service: boundaries, districts, zoning and overlays, wetlands, "
    "coastal and flood layers, soils, parcels, building footprints and trails. Data is kept in the source CRS "
    "(EPSG:2263). The service warns it contains draft data that may be incomplete. "
    "See [AGENTS.md](AGENTS.md) for how the catalog is organised and how to query it.")
titles = {c[0]: c[1] for c in collections}
for link in cat_json["links"]:
    if link["rel"] == "root":
        link["title"] = cat_json["title"]
    if link["rel"] == "child":
        link["title"] = titles[link["href"].split("/")[1]]
(ROOT / "catalog.json").write_text(json.dumps(cat_json, indent=2) + "\n")

rmeta_path = ROOT / ".portolan" / "metadata.yaml"
rmeta = yaml.safe_load(rmeta_path.read_text())
rmeta["processing_notes"] = NOTES
rmeta_path.write_text(yaml.safe_dump(rmeta, sort_keys=False, allow_unicode=True, width=100))

join_sql = ("SELECT p.SCTM, a.Zoning, a.AHO, a.LBO, p.geometry\n"
            "FROM read_parquet('ehtaxmap/ehtaxmap.parquet') p\n"
            "JOIN read_parquet('aho_lbo/aho_lbo.parquet') a ON a.SCTM = p.SCTM;")
con.execute(join_sql).fetchall()
n_tax, n_aho, n_join, d_tax, d_aho = q(
    "select (select count(*) from read_parquet('ehtaxmap/ehtaxmap.parquet')),"
    "(select count(*) from read_parquet('aho_lbo/aho_lbo.parquet')),"
    f"(select count(*) from ({join_sql.rstrip(';')})),"
    "(select count(distinct SCTM) from read_parquet('ehtaxmap/ehtaxmap.parquet')),"
    "(select count(distinct SCTM) from read_parquet('aho_lbo/aho_lbo.parquet'))")[0]

R = ["# AGENTS.md — East Hampton, NY GIS Layers (mirror)\n",
     "Guidance for AI agents and LLMs working with this catalog.\n",
     "## Overview\n",
     f"A mirror of the Town of East Hampton, New York's [MapServiceForOpenGov]({SERVICE}) ArcGIS MapServer. "
     f"Each feature layer is one collection holding one GeoParquet file. {len(collections)} collections, "
     f"{total:,} features in total, extracted on {EXTRACTED}.\n",
     "The service describes itself as built \"for the express intent of being used in the Town's Open Gov "
     "application\" and says it \"contains draft data that may be incomplete\". Treat the layers as a "
     "convenience copy, not an authoritative record.\n",
     "## Collections\n",
     "Group is the layer group in the source service, where one exists.\n",
     "| Collection | Source layer | Group | Geometry | Features |",
     "|---|---|---|---|---|"]
for cid, name, lid, group, gtype, n in sorted(collections, key=lambda c: (c[3] or "", c[1])):
    R.append(f"| [{cid}]({cid}/AGENTS.md) | [{md_escape(name)}]({SERVICE}/{lid}) | {md_escape(group or '')} "
             f"| {gtype} | {n:,} |")
R += ["",
      "Not mirrored: layer 45 (Pool Points) failed extraction because some points have `NaN` coordinates; "
      "layer 81 duplicates layer 56 (EH Waterbodies); the six group layers (18, 32, 47, 53, 63, 69) hold no data.\n",
      "## Data access patterns\n",
      "- One GeoParquet file per collection at `<collection>/<collection>.parquet`.",
      "- CRS is EPSG:2263 (NAD83 / New York Long Island, US survey feet) for every file. Reproject with "
      "`ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true)` for web maps.",
      "- The `geometry` column is WKB. `bbox` is a per-row bounding box. Where a `Shape` column exists it is a "
      "leftover ArcGIS field and is NULL.",
      "- The data files are not stored in git. They are meant for Azure blob storage "
      "(`https://flatgeobuf.blob.core.windows.net/easthampton/`), which is not live yet. Until then, the "
      "queries in each collection's AGENTS.md need local copies of the files.\n",
      "```sql\nINSTALL spatial; LOAD spatial;\n"
      "SELECT count(*) AS parcels FROM read_parquet('ehtaxmap/ehtaxmap.parquet');\n```\n",
      "## Joining layers\n",
      f"`ehtaxmap` (tax parcels, {n_tax:,} rows) and `aho_lbo` ({n_aho:,} rows) both carry `SCTM`, the Suffolk "
      f"County tax map number. `ehtaxmap` has {d_tax:,} distinct values and `aho_lbo` {d_aho:,}, so one value "
      f"repeats and a join on `SCTM` returns {n_join:,} rows. `aho_lbo` adds the `Zoning`, `AHO` and `LBO` "
      "columns:\n",
      "```sql\n" + join_sql + "\n```\n",
      "## License\n",
      "The service publishes no license. Its copyright text is carried verbatim as the attribution in the "
      "[README](README.md), and the license is recorded as `other`. The copyright text says the parcel linework "
      "is used with permission of the Suffolk County Real Property Tax Service Agency.\n"]
(ROOT / "AGENTS.md").write_text("\n".join(R))

# portolan 0.8.0 prefixes collection links in the root README with the catalog directory name.
subprocess.run(["portolan", "readme"], check=True, capture_output=True)
readme = (ROOT / "README.md").read_text().replace(f"]({ROOT.name}/", "](")
(ROOT / "README.md").write_text(readme)
print(f"{len(collections)} collections, {total} features; join {n_join}")
