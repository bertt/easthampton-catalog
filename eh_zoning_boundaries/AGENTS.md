# AGENTS.md — EH Zoning Boundaries

Guidance for working with the `eh_zoning_boundaries` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "EH Zoning Boundaries" layer (layer 82, in the service's "EH Zoning" group) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 458 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete. The publisher describes it as: "This data shows the Zoning regions for the Town of East Hampton NY. This is a polygon dataset. It was created by combining the parcel boundaries within a region demarcated by the zoning lines. If parcels were split by the zoning line this boundary was adjusted accordingly. This layer is updated as the zoning is updated. This is not the official zoning for the Town. This is just one piece that makes up the Towns larger comprehensive zoning. The Towns legal zoning is represented on the official published maps, as it is directed in the Town Code." Credit given by the publisher on this layer: TOEH IT Dept GIS Division, Barnaby Friedman.

- Source layer: [EH Zoning Boundaries](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/82) (layer id 82).
- Rows: 458. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2852, 40.9238, -71.8561, 41.1248.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('eh_zoning_boundaries/eh_zoning_boundaries.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Not documented by the publisher. | 0 | 458 |
| `Zoning` | string | Not documented by the publisher. | 0 | 14 |
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
FROM read_parquet('eh_zoning_boundaries/eh_zoning_boundaries.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('eh_zoning_boundaries/eh_zoning_boundaries.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
