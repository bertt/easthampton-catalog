# AGENTS.md — Cobra Zones

Guidance for working with the `cobra_zones` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "Cobra Zones" layer (layer 34, in the service's "FEMA DFIRM Published 9-25-09" group) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 211 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [Cobra Zones](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/34) (layer id 34).
- Rows: 211. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -73.7358, 40.5668, -71.8503, 41.2726.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('cobra_zones/cobra_zones.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Alias in the source service: "FID". | 0 | 211 |
| `Unit` | string | Not documented by the publisher. | 0 | 95 |
| `CBRS_Type` | string | Not documented by the publisher. | 0 | 2 |
| `FI_Date` | timestamp[ms] | Not documented by the publisher. | 0 | 6 |
| `SU_Date` | timestamp[ms] | Not documented by the publisher. | 85 | 5 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `CBRS_Type`: `System Unit` (126), `Otherwise Protected Area` (85)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `CBRS_Type`:

```sql
SELECT "CBRS_Type", count(*) AS features
FROM read_parquet('cobra_zones/cobra_zones.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('cobra_zones/cobra_zones.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('cobra_zones/cobra_zones.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
