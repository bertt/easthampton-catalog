# AGENTS.md — NYS DEC Tidal Wetlands

Guidance for working with the `nys_dec_tidal_wetlands` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "NYS DEC Tidal Wetlands" layer (layer 27) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 466 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [NYS DEC Tidal Wetlands](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/27) (layer id 27).
- Rows: 466. Geometry: Polygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.3017, 40.9077, -71.8527, 41.1398.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('nys_dec_tidal_wetlands/nys_dec_tidal_wetlands.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 466 |
| `TWCAT74` | string | Not documented by the publisher. | 0 | 9 |
| `ACREAGE74` | double | Alias in the source service: "ACREAGE". | 0 | 422 |
| `Area` | double | Alias in the source service: "GIS_PUBLISHED.GISMASTER.NYSDEC_Tidal_Wetlands_EH.Area". | 466 | 0 |
| `TW_Desig` | string | Alias in the source service: "Tidal Wetland Designations". | 0 | 9 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

### Observed values of low-cardinality text columns

Computed from the mirrored data, so they describe this snapshot and may differ upstream.

- `TWCAT74`: `IM` (169), `HM` (117), `AA` (62), `FM` (44), `SM` (40), `LZ` (20), `DS` (9), `FC` (4), `HL` (1)
- `TW_Desig`: `Intertidal Marsh` (169), `High Marsh Or Salt Meadow` (117), `Adjacent Area` (62), `Coastal Fresh Marsh` (44), `Coastal Shoals, Bars And Mudflats` (40), `Littoral Zone` (20), `Dredge Spoil` (9), `Formerly Connected Tidal Wetlands` (4), `Hole Area, Does Not Contain Tidal Wetlands Or Adjacent Areas` (1)

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Features per `TWCAT74`:

```sql
SELECT "TWCAT74", count(*) AS features
FROM read_parquet('nys_dec_tidal_wetlands/nys_dec_tidal_wetlands.parquet')
GROUP BY 1 ORDER BY 2 DESC;
```

Total area in acres, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Area(geometry)) / 43560, 1) AS acres
FROM read_parquet('nys_dec_tidal_wetlands/nys_dec_tidal_wetlands.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('nys_dec_tidal_wetlands/nys_dec_tidal_wetlands.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
