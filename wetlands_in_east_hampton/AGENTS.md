# AGENTS.md — Wetlands In East Hampton

Guidance for working with the `wetlands_in_east_hampton` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "Wetlands In East Hampton" layer (layer 48, in the service's "Town Wetlands" group) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 3,041 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete. The publisher describes it as: "This layer shows wetland boundaries that have been flagged and surveyed in theTown of East Hampton. The wetland boundaries were digitized from surveys which were georeferenced in the GIS. The flagged wetlands were verified by the Planning department when they were shown on the original surveys.The majority of historic surveys have been georeferenced and the subsequent wetland boundaries have been digitized and added to the layer. The data is continually updated as new surveys are submitted to the Town. The layer is limited to the records the Town Planning department has. There may be wetlands that are not mapped on this layer as the Town does not have survey records for them." Credit given by the publisher on this layer: TOEH IT Department GIS, TOEH Planning Department, Lisa D'Andrea.

- Source layer: [Wetlands In East Hampton](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/48) (layer id 48).
- Rows: 3,041. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2659, 40.9260, -71.8698, 41.0750.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('wetlands_in_east_hampton/wetlands_in_east_hampton.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Alias in the source service: "FID". | 0 | 3,041 |
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
FROM read_parquet('wetlands_in_east_hampton/wetlands_in_east_hampton.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('wetlands_in_east_hampton/wetlands_in_east_hampton.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
