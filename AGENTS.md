# AGENTS.md — East Hampton, NY GIS Layers (mirror)

Guidance for AI agents and LLMs working with this catalog.

## Overview

A mirror of the Town of East Hampton, New York's [MapServiceForOpenGov](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer) ArcGIS MapServer. Each feature layer is one collection holding one GeoParquet file. 51 collections, 112,731 features in total, extracted on 2026-10-21.

The service describes itself as built "for the express intent of being used in the Town's Open Gov application" and says it "contains draft data that may be incomplete". Treat the layers as a convenience copy, not an authoritative record.

## Collections

Group is the layer group in the source service, where one exists.

| Collection | Source layer | Group | Geometry | Features |
|---|---|---|---|---|
| [building_footprints](building_footprints/AGENTS.md) | [Building Footprints](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/46) |  | MultiPolygon | 40,404 |
| [coastal_erosion_overlay_zones](coastal_erosion_overlay_zones/AGENTS.md) | [Coastal Erosion Overlay Zones](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/13) |  | LineString | 478 |
| [eh_cea](eh_cea/AGENTS.md) | [EH CEA](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/23) |  | MultiPolygon | 8 |
| [eh_ceha_line](eh_ceha_line/AGENTS.md) | [EH CEHA Line](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/30) |  | LineString | 61 |
| [eh_fire_districts](eh_fire_districts/AGENTS.md) | [EH Fire Districts](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/9) |  | MultiPolygon | 11 |
| [eh_historic_districts](eh_historic_districts/AGENTS.md) | [EH Historic Districts](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/11) |  | MultiPolygon | 4 |
| [eh_school_districts](eh_school_districts/AGENTS.md) | [EH School Districts](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/10) |  | MultiPolygon | 6 |
| [eh_soils](eh_soils/AGENTS.md) | [EH Soils](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/31) |  | Polygon | 545 |
| [eh_waterbodies](eh_waterbodies/AGENTS.md) | [EH Waterbodies](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/56) |  | MultiPolygon | 195 |
| [ehtaxmap](ehtaxmap/AGENTS.md) | [EHTaxMap](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/58) |  | MultiPolygon | 25,481 |
| [groundwater_zone_v](groundwater_zone_v/AGENTS.md) | [Groundwater Zone V](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/17) |  | Polygon | 1 |
| [hpod](hpod/AGENTS.md) | [HPOD](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/14) |  | MultiPolygon | 26 |
| [municipal_boundary_lines](municipal_boundary_lines/AGENTS.md) | [Municipal Boundary Lines](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/2) |  | LineString | 3 |
| [nys_dec_tidal_wetlands](nys_dec_tidal_wetlands/AGENTS.md) | [NYS DEC Tidal Wetlands](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/27) |  | Polygon | 466 |
| [nysdec_freshwater_wetlands](nysdec_freshwater_wetlands/AGENTS.md) | [NYSDEC Freshwater Wetlands](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/28) |  | Polygon | 592 |
| [national_wetland_inventory_layers_for_eh_town](national_wetland_inventory_layers_for_eh_town/AGENTS.md) | [National Wetland Inventory Layers for EH Town](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/29) |  | Polygon | 2,625 |
| [pep_boundary](pep_boundary/AGENTS.md) | [PEP Boundary](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/25) |  | Polygon | 1 |
| [pep_cnra_boundaries](pep_cnra_boundaries/AGENTS.md) | [PEP CNRA Boundaries](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/24) |  | MultiPolygon | 17 |
| [sgpa](sgpa/AGENTS.md) | [SGPA](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/16) |  | Polygon | 2 |
| [trails](trails/AGENTS.md) | [Trails](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/43) |  | LineString | 1,108 |
| [village_boundaries](village_boundaries/AGENTS.md) | [Village Boundaries](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/37) |  | Polygon | 2 |
| [wrod](wrod/AGENTS.md) | [WROD](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/15) |  | Polygon | 4 |
| [protected_veg_buffer_areas](protected_veg_buffer_areas/AGENTS.md) | [Protected veg-buffer areas](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/55) | Digitized Easements | Polygon | 23 |
| [scenic_conservation_easements](scenic_conservation_easements/AGENTS.md) | [Scenic-Conservation Easements](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/54) | Digitized Easements | MultiPolygon | 1,410 |
| [eh_boundary](eh_boundary/AGENTS.md) | [EH Boundary](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/79) | EH Base Layers | Polygon | 2 |
| [eh_right_of_ways](eh_right_of_ways/AGENTS.md) | [EH Right of Ways](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/70) | EH Base Layers | MultiPolygon | 1 |
| [fire_departments](fire_departments/AGENTS.md) | [Fire Departments](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/73) | EH Base Layers | Polygon | 9 |
| [gardiners_island_boundary](gardiners_island_boundary/AGENTS.md) | [Gardiners Island Boundary](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/78) | EH Base Layers | Polygon | 13 |
| [protected_ag_land](protected_ag_land/AGENTS.md) | [Protected Ag Land](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/74) | EH Base Layers | MultiPolygon | 71 |
| [recreational_open_space](recreational_open_space/AGENTS.md) | [Recreational Open Space](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/75) | EH Base Layers | Polygon | 1,961 |
| [school_properties](school_properties/AGENTS.md) | [School Properties](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/72) | EH Base Layers | Polygon | 21 |
| [suffolk_county_boundary](suffolk_county_boundary/AGENTS.md) | [Suffolk County Boundary](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/80) | EH Base Layers | Polygon | 70 |
| [town_facilities](town_facilities/AGENTS.md) | [Town Facilities](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/71) | EH Base Layers | Polygon | 43 |
| [villages](villages/AGENTS.md) | [Villages](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/77) | EH Base Layers | Polygon | 2 |
| [aho_lbo](aho_lbo/AGENTS.md) | [AHO & LBO](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/66) | EH Zoning | MultiPolygon | 25,481 |
| [agricultural_overlay_district](agricultural_overlay_district/AGENTS.md) | [Agricultural Overlay District](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/67) | EH Zoning | MultiPolygon | 20 |
| [eh_zoning_boundaries](eh_zoning_boundaries/AGENTS.md) | [EH Zoning Boundaries](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/82) | EH Zoning | MultiPolygon | 458 |
| [recreation_overlay_district](recreation_overlay_district/AGENTS.md) | [Recreation Overlay District](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/68) | EH Zoning | Polygon | 1 |
| [cobra_zones](cobra_zones/AGENTS.md) | [Cobra Zones](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/34) | FEMA DFIRM Published 9-25-09 | MultiPolygon | 211 |
| [fema_firm_zones](fema_firm_zones/AGENTS.md) | [FEMA FIRM Zones](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/36) | FEMA DFIRM Published 9-25-09 | Polygon | 4,796 |
| [limwa_limit_of_moderate_wave_action](limwa_limit_of_moderate_wave_action/AGENTS.md) | [LiMWA (Limit of Moderate Wave Action)](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/33) | FEMA DFIRM Published 9-25-09 | LineString | 1,079 |
| [shoreline](shoreline/AGENTS.md) | [Shoreline](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/35) | FEMA DFIRM Published 9-25-09 | LineString | 803 |
| [eh_significant_coastal_fish_wildlife_habitat](eh_significant_coastal_fish_wildlife_habitat/AGENTS.md) | [EH Significant Coastal Fish & Wildlife Habitat](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/21) | LWRP Significant Coastal Fish & Widlife Habitat | MultiPolygon | 24 |
| [ecological_complexes_boundary_line](ecological_complexes_boundary_line/AGENTS.md) | [Ecological Complexes & Boundary Line](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/19) | LWRP Significant Coastal Fish & Widlife Habitat | LineString | 11 |
| [reach_boundaries](reach_boundaries/AGENTS.md) | [Reach Boundaries](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/22) | LWRP Significant Coastal Fish & Widlife Habitat | MultiPolygon | 24 |
| [scfwh_coastal_boundary](scfwh_coastal_boundary/AGENTS.md) | [SCFWH Coastal Boundary](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/20) | LWRP Significant Coastal Fish & Widlife Habitat | LineString | 3 |
| [historcal_wetlands](historcal_wetlands/AGENTS.md) | [Historcal Wetlands](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/50) | Town Wetlands | MultiPolygon | 40 |
| [upland_areas](upland_areas/AGENTS.md) | [Upland Areas](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/52) | Town Wetlands | MultiPolygon | 58 |
| [watercourses](watercourses/AGENTS.md) | [Watercourses](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/51) | Town Wetlands | LineString | 274 |
| [wetlands_in_east_hampton](wetlands_in_east_hampton/AGENTS.md) | [Wetlands In East Hampton](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/48) | Town Wetlands | MultiPolygon | 3,041 |
| [wetlands_not_georeferenced](wetlands_not_georeferenced/AGENTS.md) | [Wetlands Not Georeferenced](https://eh-gis.ehamptonny.gov/arcgis/rest/services/MapServiceForOpenGov/MapServer/49) | Town Wetlands | MultiPolygon | 741 |

Not mirrored: layer 45 (Pool Points) failed extraction because some points have `NaN` coordinates; layer 81 duplicates layer 56 (EH Waterbodies); the six group layers (18, 32, 47, 53, 63, 69) hold no data.

## Data access patterns

- One GeoParquet file per collection at `<collection>/<collection>.parquet`.
- CRS is EPSG:2263 (NAD83 / New York Long Island, US survey feet) for every file. Reproject with `ST_Transform(geometry, 'EPSG:2263', 'EPSG:4326', always_xy := true)` for web maps.
- The `geometry` column is WKB. `bbox` is a per-row bounding box. Where a `Shape` column exists it is a leftover ArcGIS field and is NULL.
- The data files are not stored in git. They are meant for Azure blob storage (`https://flatgeobuf.blob.core.windows.net/easthampton/`), which is not live yet. Until then, the queries in each collection's AGENTS.md need local copies of the files.

```sql
INSTALL spatial; LOAD spatial;
SELECT count(*) AS parcels FROM read_parquet('ehtaxmap/ehtaxmap.parquet');
```

## Joining layers

`ehtaxmap` (tax parcels, 25,481 rows) and `aho_lbo` (25,481 rows) both carry `SCTM`, the Suffolk County tax map number. `ehtaxmap` has 25,480 distinct values and `aho_lbo` 25,480, so one value repeats and a join on `SCTM` returns 25,483 rows. `aho_lbo` adds the `Zoning`, `AHO` and `LBO` columns:

```sql
SELECT p.SCTM, a.Zoning, a.AHO, a.LBO, p.geometry
FROM read_parquet('ehtaxmap/ehtaxmap.parquet') p
JOIN read_parquet('aho_lbo/aho_lbo.parquet') a ON a.SCTM = p.SCTM;
```

## License

The service publishes no license. Its copyright text is carried verbatim as the attribution in the [README](README.md), and the license is recorded as `other`. The copyright text says the parcel linework is used with permission of the Suffolk County Real Property Tax Service Agency.
