# AGENTS.md — EHTaxMap

Guidance for working with the `ehtaxmap` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "EHTaxMap" layer (layer 58) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 25,481 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete. Credit given by the publisher on this layer: Suffolk County Real Property Tax Service COPYRIGHT 2015, COUNTY OF SUFFOLK, N.Y. Real Property Taxmap parcel linework used with permission of Suffolk County Real Property Tax Service Agency (R.P.T.S.A.).

- Source layer: [EHTaxMap](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/58) (layer id 58).
- Rows: 25,481. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2960, 40.9238, -71.8561, 41.1248.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('ehtaxmap/ehtaxmap.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 25,481 |
| `DSBL` | string | Not documented by the publisher. | 0 | 25,481 |
| `P_ID` | double | Alias in the source service: "P_ID Govern Match". | 1,277 | 24,204 |
| `GIS_ZIP_CODE` | string | Not documented by the publisher. | 2 | 6 |
| `SCTM` | string | Not documented by the publisher. | 0 | 25,480 |
| `CLASS` | string | Not documented by the publisher. | 1,391 | 138 |
| `Acres` | double | Not documented by the publisher. | 0 | 25,265 |
| `Area_Sq_Ft` | double | Not documented by the publisher. | 0 | 25,327 |
| `BTCAMP` | double | Not documented by the publisher. | 0 | 14 |
| `Zoning` | string | Alias in the source service: "ZONING". | 3 | 55 |
| `School_District` | double | Not documented by the publisher. | 0 | 6 |
| `Fire_District` | double | Not documented by the publisher. | 3 | 10 |
| `Adjacent_Public_Water` | double | Not documented by the publisher. | 22 | 2 |
| `Affordable_Housing_Overlay` | double | Not documented by the publisher. | 50 | 2 |
| `Limited_Business_Overlay` | double | Not documented by the publisher. | 50 | 2 |
| `Agricultural_District` | double | Not documented by the publisher. | 48 | 2 |
| `Water_Recharge` | double | Not documented by the publisher. | 20 | 2 |
| `HPOD` | double | Alias in the source service: "Harbor Protection Overlay District". | 48 | 2 |
| `Recreation_Overlay_District` | double | Not documented by the publisher. | 51 | 2 |
| `Coastal_Zone` | string | Not documented by the publisher. | 23,942 | 6 |
| `H2OZoneV` | double | Not documented by the publisher. | 15 | 2 |
| `SGPA` | double | Alias in the source service: "Special Groundwater Protection Area". | 12 | 2 |
| `Pine_Barren_Region` | double | Not documented by the publisher. | 10 | 2 |
| `LWRP_EH_Coastal_Boundary` | double | Not documented by the publisher. | 51 | 3 |
| `Land_Acquisition` | string | Not documented by the publisher. | 103 | 77 |
| `Nature_Preserves` | double | Not documented by the publisher. | 52 | 2 |
| `Nature_Conservancy` | string | Not documented by the publisher. | 88 | 6 |
| `Historic_Site` | double | Not documented by the publisher. | 59 | 2 |
| `Historic_Name` | string | Not documented by the publisher. | 109 | 251 |
| `NR_Lot_Inspection_File` | string | Not documented by the publisher. | 19,816 | 25 |
| `Clearing` | string | Not documented by the publisher. | 5,102 | 7 |
| `Old_File_Map` | string | Not documented by the publisher. | 58 | 64 |
| `Filed_Subdivision` | string | Not documented by the publisher. | 61 | 345 |
| `Filed_Subdivision_Name` | string | Not documented by the publisher. | 766 | 357 |
| `Filed_Subwaiver` | string | Not documented by the publisher. | 74 | 127 |
| `Filed_Subwaiver_Name` | string | Not documented by the publisher. | 826 | 128 |
| `Perimeter` | double | Not documented by the publisher. | 1 | 25,303 |
| `Historic_Districts` | string | Not documented by the publisher. | 25,294 | 5 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `GIS_ZIP_CODE`: `11937` (14,815), `11954` (5,360), `11930` (2,883), `11975` (1,418), `11963` (997), ` ` (6)
- `Coastal_Zone`: `2` (936), `4` (234), `1` (198), `3` (144), `2-4` (15), `2-3` (12)
- `Nature_Conservancy`: ` ` (23,380), `0` (1,883), `FEE` (96), `EASEMENT` (32), `` (1), ` 0` (1)
- `Clearing`: `I` (7,876), `C` (6,765), `U` (4,387), `P` (614), `E` (365), `V` (338), `I - Improved, Partially Cleared` (34)
- `Historic_Districts`: `Amagansett` (83), `Springs` (47), `Bluff Road` (34), `Montauk` (22), `<Null>` (1)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `GIS_ZIP_CODE`:

```sql
SELECT "GIS_ZIP_CODE", count(*) AS features
FROM read_parquet('ehtaxmap/ehtaxmap.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('ehtaxmap/ehtaxmap.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('ehtaxmap/ehtaxmap.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
