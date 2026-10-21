# AGENTS.md — EH Fire Districts

Guidance for working with the `eh_fire_districts` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "EH Fire Districts" layer (layer 9) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 11 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [EH Fire Districts](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/9) (layer id 9).
- Rows: 11. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2852, 40.9238, -71.8561, 41.1248.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('eh_fire_districts/eh_fire_districts.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 11 |
| `ID` | string | Not documented by the publisher. | 0 | 9 |
| `Fire_Dist_Name` | string | Not documented by the publisher. | 0 | 9 |
| `Area_Sq_Ft` | double | Not documented by the publisher. | 0 | 11 |
| `Acres` | double | Not documented by the publisher. | 0 | 11 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `ID`: `13` (2), `17` (2), `12` (1), `18` (1), `11` (1), `16` (1), `14` (1), `10` (1), `15` (1)
- `Fire_Dist_Name`: `Montauk Fire Protection` (2), `Springs Fire` (2), `Montauk Fire` (1), `Amagansett Fire` (1), `Promised Land Fire Protection` (1), `Bridgehampton Fire` (1), `East Hampton Water Supply` (1), `East Hampton Road Fire Protection` (1), `Northwest Fire Protection` (1)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `ID`:

```sql
SELECT "ID", count(*) AS features
FROM read_parquet('eh_fire_districts/eh_fire_districts.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('eh_fire_districts/eh_fire_districts.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('eh_fire_districts/eh_fire_districts.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
