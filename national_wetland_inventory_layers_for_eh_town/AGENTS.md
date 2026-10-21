# AGENTS.md — National Wetland Inventory Layers for EH Town

Guidance for working with the `national_wetland_inventory_layers_for_eh_town` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "National Wetland Inventory Layers for EH Town" layer (layer 29) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 2,625 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [National Wetland Inventory Layers for EH Town](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/29) (layer id 29).
- Rows: 2,625. Geometry: Polygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.3745, 40.8751, -71.7495, 41.1251.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('national_wetland_inventory_layers_for_eh_town/national_wetland_inventory_layers_for_eh_town.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 2,625 |
| `AREA` | double | Alias in the source service: "GIS_PUBLISHED.GISMASTER.EH_NWI.AREA". | 2,625 | 0 |
| `ATTRIBUTE` | string | Not documented by the publisher. | 0 | 145 |
| `Acres` | double | Not documented by the publisher. | 0 | 2,625 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('national_wetland_inventory_layers_for_eh_town/national_wetland_inventory_layers_for_eh_town.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('national_wetland_inventory_layers_for_eh_town/national_wetland_inventory_layers_for_eh_town.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
