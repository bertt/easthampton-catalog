# AGENTS.md — Building Footprints

Guidance for working with the `building_footprints` collection. Catalog-wide context is in the [root AGENTS.md](../AGENTS.md).

## Overview

Mirror of the "Building Footprints" layer (layer 46) of the Town of East Hampton's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS service. 40,404 polygon features, kept in the source CRS EPSG:2263. The service warns that it contains draft data that may be incomplete. The publisher describes it as: "The Building Outline Creation products provide a two dimensional digital representation of the shape of a structure. Using Pictometry imagery, a polygon shape corresponding to the visible edges of a structure’s roof is created for each qualifying structure.The collection of polygon shapes are georeferenced and delivered in geodatabase and shapefile format. The initial published data is accurate as to the fly of April 2018. Footprints are continually updated by the Town of East Hampton from that point forward, so as to reflect the most recent changes.When visible, the following types of structures measuring at least 150sq.feet (14sq.meters) and at least five pixels wide (based on 12”(30cm) or better GSD imagery) are included:Residential, commercial and industrial buildingsAttached decks or porches that have a roof or railing or that are visibly raisedIsolated garages, mobile homes, shedsGreenhousesGrain silos and oil storage tanksBuildings under construction that at least have wallsTrailer boxes with windows or doors (construction field offices)Other features with a roofThe Building Outlines produced correspond to the edges of the structure’s roof.The Building Outlines are positioned on to the imagery based on the roof location unless the base of the building isclearly visible in which case the outline is shifted to align to the visible base.Specifications are based on use of 12-inch(30cm) or better GSD Pictometry-acquired imageryPositional accuracy: offset from the imagery less than or equal to five pixelsGeometric accuracy: length of untraced edges less than or equal to five pixelsError rate: ratio of positionally or geometrically inaccurate buildings and missed buildings less than or equalto 0.5%Project Period May -June 2018Number of Parcels 25,605Base Image Acquisition Apr 2018Base Imagery Source Acquired by PictometryNumber of Buildings 29,313"

- Source layer: [Building Footprints](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/46) (layer id 46).
- Rows: 40,404. Geometry: MultiPolygon. CRS: EPSG:2263 (NAD83 / New York Long Island, US survey feet).
- Bounding box (EPSG:4326): -72.2957, 40.9253, -71.8567, 41.1002.

## Accessing the data

Run from the catalog root. Spatial functions need `INSTALL spatial; LOAD spatial;`.

```sql
SELECT count(*) AS features FROM read_parquet('building_footprints/building_footprints.parquet');
```

## Schema & field notes

Types come from the GeoParquet file. Alias and coded-value text is copied from the source layer's field metadata. Where the source gives no alias or code list, the column is listed without a meaning: the publisher has not documented it, and this catalog does not guess.

| Column | Type | Meaning from the source | Nulls | Distinct |
|---|---|---|---|---|
| `OBJECTID` | int64 | Alias in the source service: "FID". | 0 | 40,404 |
| `DSBL` | string | Not documented by the publisher. | 13,624 | 17,729 |
| `AREA` | double | Alias in the source service: "GIS_PUBLISHED.GISMASTER.EH_BuildingFootprints_Edit.AREA". | 40,404 | 0 |
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
FROM read_parquet('building_footprints/building_footprints.parquet');
```

Reproject to WGS84 for web maps:

```sql
SELECT ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true) AS geom_4326
FROM read_parquet('building_footprints/building_footprints.parquet')
LIMIT 5;
```

## Related collections

The source service defines no foreign keys between layers. See the [root AGENTS.md](../AGENTS.md) for the one join this catalog documents.
