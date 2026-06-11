import geopandas as gpd
import pandas as pd
import osmnx as ox


def load_buildings(county_names):
    """
    Download OSM building footprints for a list of counties.
    """

    gdfs = []

    for place in county_names:
        gdf = ox.features_from_place(
            place,
            tags={"building": True}
        )

        # keep only polygonal buildings
        gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]

        gdfs.append(gdf)

    return pd.concat(gdfs, ignore_index=True)


def compute_building_features(
    tracts_gdf: gpd.GeoDataFrame,
    county_names,
    projected_crs="EPSG:5070"
):
    """
    Adds:
        - building_count
        - building_density
        - building_coverage_ratio
        - mean_building_area
    """

    tracts = tracts_gdf.to_crs(projected_crs)

    buildings = load_buildings(county_names)
    buildings = gpd.GeoDataFrame(buildings, geometry="geometry", crs="EPSG:4326")
    buildings = buildings.to_crs(projected_crs)

    # ensure tract area exists
    if "land_area_km2" not in tracts.columns:
        tracts["land_area_km2"] = tracts.geometry.area / 1e6

    area = tracts.set_index("tract_id")["land_area_km2"]

    # -----------------------------------
    # Spatial join: buildings → tracts
    # -----------------------------------
    buildings_in_tracts = gpd.sjoin(
        buildings,
        tracts[["tract_id", "geometry"]],
        predicate="within"
    )

    # -----------------------------------
    # BUILDING COUNT
    # -----------------------------------
    building_count = (
        buildings_in_tracts.groupby("tract_id").size()
        .rename("building_count")
    )

    # -----------------------------------
    # BUILDING AREA
    # -----------------------------------
    buildings_in_tracts["building_area_m2"] = (
        buildings_in_tracts.geometry.area
    )

    mean_building_area = (
        buildings_in_tracts.groupby("tract_id")["building_area_m2"].mean()
        .rename("mean_building_area")
    )

    # total built-up area per tract
    built_area = (
        buildings_in_tracts.groupby("tract_id")["building_area_m2"].sum()
    )

    # -----------------------------------
    # DENSITIES / RATIOS
    # -----------------------------------
    building_density = (building_count / area).rename("building_density")

    building_coverage_ratio = (
        (built_area / (tracts.set_index("tract_id")["land_area_km2"] * 1e6))
    ).rename("building_coverage_ratio")

    # -----------------------------------
    # MERGE
    # -----------------------------------
    features = pd.concat(
        [building_count, building_density, building_coverage_ratio, mean_building_area],
        axis=1
    ).reset_index()

    return tracts.merge(features, on="tract_id", how="left")