# AGENTS.md — EH CEA

Guidance for working with the `eh_cea` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "EH CEA" layer (layer 23) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 8 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [EH CEA](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/23) (layer id 23).
- Rows: 8. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.7419, 40.8936, -71.8054, 41.3108.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('eh_cea/eh_cea.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 8 |
| `LOCATION` | string | Not documented by the publisher. | 0 | 4 |
| `NAME` | string | Not documented by the publisher. | 0 | 7 |
| `AGENCY` | string | Not documented by the publisher. | 0 | 3 |
| `REGION` | string | Not documented by the publisher. | 0 | 1 |
| `REASON` | string | Not documented by the publisher. | 0 | 4 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `LOCATION`: `East Hampton` (5), `South Fork` (1), `Hither Hills` (1), `Southampton` (1)
- `NAME`: `SGPA` (2), `Accabonac Harbor` (1), `Montauk Addition` (1), `Long Pond` (1), `Hither Woods` (1), `Water Recharge` (1), `Peconic Bay and Environs` (1)
- `AGENCY`: `Suffolk County` (5), `Long Island Regional Planning` (2), `East Hampton, Town of` (1)
- `REGION`: `1` (8)
- `REASON`: `benefit to human health&protect drinking water` (4), `protect groundwater` (2), `protect groundwater & drinking water` (1), `Protect public health, water, vegetation, & scenic beauty` (1)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `LOCATION`:

```sql
SELECT "LOCATION", count(*) AS features
FROM read_parquet('eh_cea/eh_cea.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('eh_cea/eh_cea.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('eh_cea/eh_cea.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
