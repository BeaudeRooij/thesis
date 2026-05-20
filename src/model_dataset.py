import pandas as pd
import numpy as np


def safe_divide(a, b):

    return np.where(
        (b == 0) | (pd.isna(b)),
        np.nan,
        a / b
    )


def build_modeling_dataset(tracts):

    df = tracts.copy()

    # ---------------------------------------------------
    # CORE DEMOGRAPHICS
    # ---------------------------------------------------

    df["population_density"] = (
        df["total_population"]
        / df["land_area_km2"]
    )

    # 2+ vehicle households
    df["two_plus_vehicle_households"] = (
        df["two_vehicle_households"]
        + df["three_plus_vehicle_households"]
    )

    # other race category
    df["other_multiracial"] = (
        df["race_total"]
        - df["white_non_hispanic"]
        - df["black"]
        - df["asian"]
        - df["hispanic_latino"]
    )

    # ---------------------------------------------------
    # FINAL MODEL TABLE
    # ---------------------------------------------------

    final = pd.DataFrame({

        # ---------------------------------------------
        # IDENTIFIERS
        # ---------------------------------------------

        "tract_id": df["tract_id"],

        # ---------------------------------------------
        # CORE DEMOGRAPHICS
        # ---------------------------------------------

        "total_population":
            df["total_population"],

        "population_density":
            df["population_density"],

        "pct_under_18":
            df["pct_under_18"],

        "pct_18_64":
            df["pct_18_64"],

        "pct_over_65":
            df["pct_over_65"],

        "sex_ratio":
            df["sex_ratio"],

        "median_age":
            df["median_age"],

        "avg_household_size":
            df["avg_household_size"],

        "households":
            df["households"],

        # ---------------------------------------------
        # SOCIOECONOMIC
        # ---------------------------------------------

        "median_household_income":
            df["median_income"],

        "per_capita_income":
            df["per_capita_income"],

        "poverty_rate":
            df["poverty_rate"],

        "unemployment_rate":
            df["unemployment_rate"],

        "labor_force_participation_rate":
            df["labor_force_participation_rate"],

        "snap_participation_rate":
            df["snap_rate"],

        "public_assistance_rate":
            safe_divide(
                df["public_assistance_households"],
                df["households"]
            ),

        # ---------------------------------------------
        # EDUCATION
        # ---------------------------------------------

        "pct_high_school":
            df["pct_high_school"],

        "pct_bachelors_degree":
            df["pct_bachelors"],

        "pct_graduate_degree":
            df["pct_graduate_degree"],

        # ---------------------------------------------
        # TRANSPORTATION
        # ---------------------------------------------

        "pct_no_vehicle_households":
            df["pct_no_vehicle"],

        "pct_one_vehicle_households":
            safe_divide(
                df["one_vehicle_households"],
                df["households"]
            ),

        "pct_two_plus_vehicle_households":
            safe_divide(
                df["two_plus_vehicle_households"],
                df["households"]
            ),

        "median_commute_time":
            df["median_commute_time"],

        "pct_public_transit_commute":
            df["pct_transit_commute"],

        "pct_car_commute":
            safe_divide(
                df["car_commute"],
                df["workers_total"]
            ),

        "pct_walk_commute":
            df["pct_walk_commute"],

        "pct_bike_commute":
            df["pct_bike_commute"],

        "pct_work_from_home":
            df["pct_wfh"],

        # ---------------------------------------------
        # HOUSING
        # ---------------------------------------------

        "housing_units":
            df["housing_units"],

        "occupied_housing_units":
            safe_divide(
                df["occupied_units"],
                df["housing_units"]
            ),

        "vacant_housing_units":
            safe_divide(
                df["vacant_units"],
                df["housing_units"]
            ),

        "homeownership_rate":
            safe_divide(
                df["owner_occupied"],
                df["housing_units"]
            ),

        "median_rent":
            df["median_rent"],

        "median_home_value":
            df["median_home_value"],

        "housing_density":
            safe_divide(
                df["housing_units"],
                df["land_area_km2"]
            ),

        "median_year_built":
            df["median_year_built"],

        # ---------------------------------------------
        # LAND / URBAN FORM
        # ---------------------------------------------

        "land_area_km2":
            df["land_area_km2"],

        # ---------------------------------------------
        # RACE / ETHNICITY
        # ---------------------------------------------

        "pct_white_non_hispanic":
            df["pct_white_non_hispanic"],

        "pct_black":
            df["pct_black"],

        "pct_hispanic_latino":
            df["pct_hispanic_latino"],

        "pct_asian":
            df["pct_asian"],

        "pct_other_multiracial":
            safe_divide(
                df["other_multiracial"],
                df["race_total"]
            ),
    })

    # ---------------------------------------------------
    # TYPE CLEANUP
    # ---------------------------------------------------

    float_cols = final.select_dtypes(
        include=["float64"]
    ).columns

    final[float_cols] = final[
        float_cols
    ].astype("float32")

    return final