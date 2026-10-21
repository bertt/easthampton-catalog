# AGENTS.md — EH Significant Coastal Fish & Wildlife Habitat

Guidance for working with the `eh_significant_coastal_fish_wildlife_habitat` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "EH Significant Coastal Fish & Wildlife Habitat" layer (layer 21, in the service's "LWRP Significant Coastal Fish & Widlife Habitat" group) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 24 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [EH Significant Coastal Fish & Wildlife Habitat](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/21) (layer id 21).
- Rows: 24. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.3132, 40.9266, -71.7891, 41.1346.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('eh_significant_coastal_fish_wildlife_habitat/eh_significant_coastal_fish_wildlife_habitat.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 24 |
| `NAME` | string | Not documented by the publisher. | 0 | 20 |
| `TXT` | string | Not documented by the publisher. | 0 | 17 |
| `SCFWH` | string | Not documented by the publisher. | 0 | 18 |
| `LOCALLYSIG` | string | Not documented by the publisher. | 0 | 6 |
| `Area_Sq_Ft` | double | Not documented by the publisher. | 0 | 24 |
| `Acres` | double | Not documented by the publisher. | 0 | 24 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `LOCALLYSIG`: ` ` (19), `WAINSCOTT POND` (1), `MONTAUK POINT` (1), `FRESH POND BELL ESTATE WETLAND` (1), `THREE MILE HARBOR` (1), `GEORGICA POND` (1)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `LOCALLYSIG`:

```sql
SELECT "LOCALLYSIG", count(*) AS features
FROM read_parquet('eh_significant_coastal_fish_wildlife_habitat/eh_significant_coastal_fish_wildlife_habitat.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('eh_significant_coastal_fish_wildlife_habitat/eh_significant_coastal_fish_wildlife_habitat.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('eh_significant_coastal_fish_wildlife_habitat/eh_significant_coastal_fish_wildlife_habitat.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
