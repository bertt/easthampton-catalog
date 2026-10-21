"""Give each collection a readable default style with its own colour.

The extraction wrote one opaque red fill for every layer. This replaces the
paint of the single layer in styles/default.json and keeps its source, so the
PMTiles url and zoom range stay as portolan wrote them. Colours are grouped by
theme, and siblings in a theme take different hues.

Run from anywhere:  python3 tools/build_styles.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

THEMES = [
    ("water", ["wetland", "waterbod", "watercourse", "upland", "tidal", "freshwater", "national_wetland"],
     ["#1b7f9e", "#2a9d8f", "#3b6fb6", "#52a7a0", "#5b9bd5", "#2f8f83", "#4a7fb5"]),
    ("flood and coast", ["fema", "limwa", "cobra", "shoreline", "ceha", "coastal", "scfwh", "reach", "ecological",
                         "eh_cea", "cea"],
     ["#0b6e99", "#e4572e", "#7b5ea7", "#17a398", "#d1495b", "#3f88c5", "#f49d37", "#6a4c93"]),
    ("zoning and overlays", ["zoning", "aho", "overlay", "hpod", "wrod", "sgpa", "groundwater", "historic",
                             "pep_", "recreation"],
     ["#8e44ad", "#e67e22", "#c0392b", "#2c7fb8", "#d35400", "#6c5ce7", "#b5651d", "#9b2335", "#5d8aa8"]),
    ("administrative", ["boundary", "village", "district", "school", "fire", "municipal", "suffolk", "gardiners",
                        "right_of_way"],
     ["#e76f51", "#264653", "#2a9d8f", "#e9c46a", "#6d597a", "#b56576", "#355070", "#f4a261", "#457b9d"]),
    ("land and facilities", ["protected", "easement", "open_space", "preserve", "facilities", "trails",
                             "agricultural", "veg_buffer"],
     ["#4c9f50", "#7a9e3b", "#2e7d32", "#a3b18a", "#588157", "#6b8e23", "#8f9d3a"]),
]
FALLBACK = {
    "ehtaxmap": "#c7771d",
    "building_footprints": "#3d4a5c",
    "eh_soils": "#a0724a",
}

used = {}


def pick(cid):
    if cid in FALLBACK:
        return FALLBACK[cid]
    for name, keys, palette in THEMES:
        if any(k in cid for k in keys):
            i = used.get(name, 0)
            used[name] = i + 1
            return palette[i % len(palette)]
    return "#6c757d"


def darken(hex_color, f=0.65):
    h = hex_color.lstrip("#")
    return "#%02x%02x%02x" % tuple(int(int(h[i:i + 2], 16) * f) for i in (0, 2, 4))


for cdir in sorted(p for p in ROOT.iterdir() if (p / "collection.json").exists()):
    cid = cdir.name
    stac = json.loads((cdir / "collection.json").read_text())
    gtype = stac["geoparquet:geometry_type"]
    count = stac["geoparquet:feature_count"]
    style_path = cdir / "styles" / "default.json"
    style = json.loads(style_path.read_text())
    layer = style["layers"][0]
    color = pick(cid)
    if "Polygon" in gtype:
        dense = count > 5000
        layer["type"] = "fill"
        layer["paint"] = {
            "fill-color": color,
            "fill-opacity": 0.55 if not dense else 0.7,
            "fill-outline-color": darken(color),
        }
    elif "Line" in gtype:
        layer["type"] = "line"
        layer["layout"] = {"line-cap": "round", "line-join": "round"}
        layer["paint"] = {
            "line-color": color,
            "line-width": ["interpolate", ["linear"], ["zoom"], 8, 1.2, 14, 3, 18, 5],
        }
    else:
        layer["type"] = "circle"
        layer["paint"] = {"circle-color": color, "circle-radius": 3, "circle-stroke-color": "#ffffff",
                          "circle-stroke-width": 0.8}
    style["name"] = f"{stac['title']} (single colour)"
    style_path.write_text(json.dumps(style, indent=2) + "\n")
    print(cid, gtype, color)
