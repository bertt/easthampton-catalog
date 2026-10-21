# AGENTS.md — Fire Departments

Guidance for working with the `fire_departments` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "Fire Departments" layer (layer 73, in the service's "EH Base Layers" group) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 9 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [Fire Departments](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/73) (layer id 73).
- Rows: 9. Geometry: Polygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2913, 40.9687, -71.9503, 41.0502.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('fire_departments/fire_departments.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID_1` | int64 | Not documented by the publisher. | 0 | 9 |
| `LAST_NAME` | string | Not documented by the publisher. | 0 | 5 |
| `SCTM` | string | Not documented by the publisher. | 0 | 9 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `LAST_NAME`: `MONTAUK FIRE DISTRICT` (4), `SPRINGS FIRE DISTRICT` (2), `VILLAGE OF EAST HAMPTON` (1), `VILLAGE OF SAG HARBOR` (1), `AMAGANSETT FIRE DISTRICT` (1)
- `SCTM`: `300-150-3-16.001` (1), `300-48-4-17.001` (1), `302-5-1-5` (1), `300-16-2-24.004` (1), `301-4-1-10.003` (1), `300-48-4-16.002` (1), `300-62-2-18.002` (1), `300-62-2-8` (1), `300-16-2-24.002` (1)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `LAST_NAME`:

```sql
SELECT "LAST_NAME", count(*) AS features
FROM read_parquet('fire_departments/fire_departments.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('fire_departments/fire_departments.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('fire_departments/fire_departments.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
