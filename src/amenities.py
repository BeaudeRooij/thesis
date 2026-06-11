import pandas as pd
import geopandas as gpd
import osmnx as ox


# ---------------------------------------------------
# DEFAULT AMENITIES (your target features only)
# ---------------------------------------------------
AMENITIES = {
    "restaurant": {"amenity": "restaurant"},
    "cafe": {"amenity": "cafe"},
    "school": {"amenity": "school"},
    "hospital": {"amenity": "hospital"},
    "pharmacy": {"amenity": "pharmacy"},
    "supermarket": {"shop": "supermarket"},
    "park": {"leisure": "park"},
    "transit_stop": {"highway": "bus_stop"},
}


# ---------------------------------------------------
# OSM LOADER (robust)
# ---------------------------------------------------
def load_amenities_from_places(place_list, tags):
    gdfs = []

    for place in place_list:
        try:
            gdf = ox.features_from_place(place, tags=tags)

            if gdf is None or len(gdf) == 0:
                continue

            gdf = gdf[gdf.geometry.notnull()].copy()
            gdfs.append(gdf)

        except Exception as e:
            print(f"Skipping {place} | {tags} -> {e}")
            continue

    if len(gdfs) == 0:
        return None

    return pd.concat(gdfs, ignore_index=True)


# ---------------------------------------------------
# MAIN FEATURE FUNCTION (TRACT-COMPATIBLE)
# ---------------------------------------------------
def compute_amenity_features(
    tracts_gdf: gpd.GeoDataFrame,
    counties,
    projected_crs="EPSG:5070",
    amenities=AMENITIES
):
    """
    Input:
        tracts_gdf must contain:
            - tract_id
            - geometry
            - land_area_km2 (optional but recommended)

    Output:
        same GeoDataFrame + amenity density features
    """

    tracts = tracts_gdf.to_crs(projected_crs)

    # ensure area exists
    if "land_area_km2" not in tracts.columns:
        tracts["land_area_km2"] = tracts.geometry.area / 1e6

    area = tracts.set_index("tract_id")["land_area_km2"]

    feature_frames = []

    for name, tags in amenities.items():

        print(f"Processing: {name}")

        gdf = load_amenities_from_places(counties, tags)

        if gdf is None:
            continue

        # ensure CRS consistency
        gdf = gpd.GeoDataFrame(gdf, geometry="geometry", crs="EPSG:4326")
        gdf = gdf.to_crs(projected_crs)

        # spatial join using YOUR tract schema
        joined = gpd.sjoin(
            gdf,
            tracts[["tract_id", "geometry"]],
            predicate="within"
        )

        # counts per tract
        counts = (
            joined.groupby("tract_id").size()
            .rename(f"{name}_count")
        )

        # density per km²
        density = (counts / area).rename(f"{name}_density")

        feature_frames.append(
            pd.concat([counts, density], axis=1)
        )

    if len(feature_frames) == 0:
        return tracts_gdf

    features = pd.concat(feature_frames, axis=1).reset_index()

    return tracts.merge(features, on="tract_id", how="left")