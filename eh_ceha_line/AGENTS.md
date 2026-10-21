# AGENTS.md — EH CEHA Line

Guidance for working with the `eh_ceha_line` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "EH CEHA Line" layer (layer 30) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 61 line features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [EH CEHA Line](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/30) (layer id 30).
- Rows: 61. Geometry: LineString. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2660, 40.9242, -71.8565, 41.1098.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('eh_ceha_line/eh_ceha_line.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 61 |
| `LENGTH` | double | Not documented by the publisher. | 0 | 60 |
| `PHOTO` | string | Not documented by the publisher. | 0 | 55 |
| `SHEET` | string | Not documented by the publisher. | 0 | 59 |
| `TOWN` | string | Not documented by the publisher. | 0 | 1 |
| `VILLAGE` | string | Not documented by the publisher. | 0 | 2 |
| `COUNTY` | string | Not documented by the publisher. | 0 | 1 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `TOWN`: `East Hampton` (61)
- `VILLAGE`: ` ` (57), `East Hampton` (4)
- `COUNTY`: `Suffolk` (61)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `VILLAGE`:

```sql
SELECT "VILLAGE", count(*) AS features
FROM read_parquet('eh_ceha_line/eh_ceha_line.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total length in miles, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Length(geometry)) / 5280, 1) AS miles
FROM read_parquet('eh_ceha_line/eh_ceha_line.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('eh_ceha_line/eh_ceha_line.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
