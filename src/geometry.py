import geopandas as gpd
import pandas as pd


def load_tract_geometries(
    state_fips,
    county_fips_list=None,
    year=2023
):
    """
    Load Census tract geometries from TIGER/Line.

    Parameters
    ----------
    state_fips : str
        State FIPS code.

    county_fips_list : list[str] or None
        Optional county filters.

    year : int
        TIGER vintage year.

    Returns
    -------
    GeoDataFrame
    """

    print(f"Loading tract geometries for state {state_fips}...")

    url = (
        f"https://www2.census.gov/geo/tiger/TIGER{year}/"
        f"TRACT/tl_{year}_{state_fips}_tract.zip"
    )

    gdf = gpd.read_file(url)

    print("Raw tracts:", len(gdf))

    # ---------------------------------------------------
    # Filter counties
    # ---------------------------------------------------

    if county_fips_list is not None:

        gdf = gdf[
            gdf["COUNTYFP"].isin(county_fips_list)
        ].copy()

        print("Filtered tracts:", len(gdf))

    # ---------------------------------------------------
    # CRS cleanup
    # ---------------------------------------------------

    gdf = gdf.to_crs(epsg=4326)

    gdf = gdf[
        gdf.geometry.notnull()
    ].copy()

    gdf["geometry"] = gdf.buffer(0)

    gdf = gdf[
        gdf.is_valid
    ].copy()

    # ---------------------------------------------------
    # Area calculations
    # ---------------------------------------------------

    gdf_proj = gdf.to_crs(epsg=3857)

    gdf["land_area_km2"] = (
        gdf_proj.geometry.area / 1e6
    )

    # ---------------------------------------------------
    # Centroids
    # ---------------------------------------------------

    centroids = gdf_proj.centroid.to_crs(epsg=4326)

    gdf["centroid_lon"] = centroids.x
    gdf["centroid_lat"] = centroids.y

    # ---------------------------------------------------
    # Standardized IDs
    # ---------------------------------------------------

    gdf["tract_id"] = gdf["GEOID"]

    gdf["state_fips"] = gdf["tract_id"].str[:2]

    gdf["county_fips"] = gdf["tract_id"].str[2:5]

    gdf["tract_code"] = gdf["tract_id"].str[5:]

    # ---------------------------------------------------
    # Final columns
    # ---------------------------------------------------

    keep_cols = [

        "tract_id",

        "state_fips",
        "county_fips",
        "tract_code",

        "land_area_km2",

        "centroid_lat",
        "centroid_lon",

        "geometry"
    ]

    gdf = gdf[
        keep_cols
    ].copy()

    print("Geometry table ready.")

    return gdf