# AGENTS.md — Coastal Erosion Overlay Zones

Guidance for working with the `coastal_erosion_overlay_zones` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "Coastal Erosion Overlay Zones" layer (layer 13) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 478 line features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete.

- Source layer: [Coastal Erosion Overlay Zones](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/13) (layer id 13).
- Rows: 478. Geometry: LineString. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2707, 40.9238, -71.8561, 41.1248.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('coastal_erosion_overlay_zones/coastal_erosion_overlay_zones.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `Zone` | int16 | Not documented by the publisher. | 0 | 4 |
| `Object_ID` | int64 | Alias in the source service: ""Object ID"". | 0 | 478 |
| `ZoneSheets` | string | Alias in the source service: "Zone Map Sheets". | 0 | 13 |
| `geometry` | binary (WKB) | Feature geometry. | 0 | |
| `bbox` | struct | Per-row bounding box (xmin, ymin, xmax, ymax) in the file's CRS, for spatial filtering. | | |
| `Shape` | binary | Always NULL. Left over from the ArcGIS geometry field; use `geometry`. | all | |

## Data quality & usage notes

- The source service says it is built for the Town's OpenGov application and "contains draft data that may be incomplete".
- Coordinates are in EPSG:2263, in US survey feet. Areas and lengths computed from the geometry are in square feet and feet. Reproject to EPSG:4326 for web maps.
- Geometry is stored as it came from the service. Nothing was cleaned or filtered.

## Example queries

Total length in miles, computed from the geometry (EPSG:2263 is in US survey feet):

```sql
SELECT round(sum(ST_Length(geometry)) / 5280, 1) AS miles
FROM read_parquet('coastal_erosion_overlay_zones/coastal_erosion_overlay_zones.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('coastal_erosion_overlay_zones/coastal_erosion_overlay_zones.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
