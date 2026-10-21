# AGENTS.md — Trails

Guidance for working with the `trails` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "Trails" layer (layer 43) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 1,108 line features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete. The publisher describes it as: "This Feature Class contains all the Trails for the Town of East Hampton. The Data was collected, compiled and edited beginning in 2012 and continues to be constantly updated and revised at published date (Spring 2015).This data is constantly being updated and revised as trails are maintianed, routes are changed old trail may be closed and new may be opened. This data is thus considered DRAFT and constantly evolving. It is, as far as we can tell, current at its published date but discrepancies may occur moving forward as routes may be altered etc..., prior to it being recorded and reflected in the data. We make every effort to edit and keep this data updated as changes occur." Credit given by the publisher on this layer: Bob Masin, Andy Gaites, Andy Drake.

- Source layer: [Trails](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/43) (layer id 43).
- Rows: 1,108. Geometry: LineString. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2851, 40.9512, -71.8563, 41.0822.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('trails/trails.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 1,108 |
| `Trail_Name` | string | Not documented by the publisher. | 230 | 134 |
| `Trail_Loca` | string | Alias in the source service: "Trail_Location". | 7 | 137 |
| `Trail_Type` | string | Not documented by the publisher. | 13 | 11 |
| `Trail_Blaz` | string | Alias in the source service: "Trail_Blaze". | 14 | 91 |
| `Trail_Stat` | string | Alias in the source service: "Trail_Status". | 0 | 6 |
| `Miles` | double | Not documented by the publisher. | 7 | 1,065 |
| `Feet` | double | Not documented by the publisher. | 7 | 1,090 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `Trail_Type`: `Hiking Trail` (795), `Dirt Road` (190), `Paved Road` (64), `Woods Dirt Road` (16), `Paved Path` (6), `Old Road` (5), `MV Trail` (5), `Other` (5), ` ` (5), `` (3), `Horse Trail` (1)
- `Trail_Stat`: `Open` (923), `Closed` (164), `NotPublic` (13), `Other` (4), `Proposed` (3), `Trial` (1)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `Trail_Type`:

```sql
SELECT "Trail_Type", count(*) AS features
FROM read_parquet('trails/trails.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total length in miles, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Length(geometry)) / 5280, 1) AS miles
FROM read_parquet('trails/trails.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('trails/trails.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
