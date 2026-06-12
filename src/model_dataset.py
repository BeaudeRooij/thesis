import pandas as pd
import numpy as np


def safe_divide(a, b):
    a = np.asarray(a, dtype="float64")
    b = np.asarray(b, dtype="float64")

    return np.where(
        (b == 0) | np.isnan(b),
        np.nan,
        a / b
    )


def build_modeling_dataset(tracts):

    df = tracts.copy()

    # Core derived features
    df["population_density"] = safe_divide(
        df["total_population"],
        df["land_area_km2"]
    )

    df["two_plus_vehicle_households"] = (
        df["two_vehicle_households"] +
        df["three_plus_vehicle_households"]
    )

    df["other_multiracial"] = (
        df["race_total"]
        - df["white_non_hispanic"]
        - df["black"]
        - df["asian"]
        - df["hispanic_latino"]
    )

    # Final model table
    final = pd.DataFrame({

        # id
        "tract_id": df["tract_id"],

        # Core demographics
        "total_population": df["total_population"],
        "population_density": df["population_density"],

        "pct_under_18": df["pct_under_18"],
        "pct_18_64": df["pct_18_64"],
        "pct_over_65": df["pct_over_65"],

        "sex_ratio": df["sex_ratio"],
        "median_age": df["median_age"],
        "avg_household_size": df["avg_household_size"],

        "households": df["households"],

        # Socioeconomic
        "median_household_income": df["median_income"],
        "per_capita_income": df["per_capita_income"],

        "poverty_rate": df["poverty_rate"],
        "unemployment_rate": df["unemployment_rate"],
        "labor_force_participation_rate": df["labor_force_participation_rate"],
        "snap_participation_rate": df["snap_rate"],

        "public_assistance_rate": safe_divide(
            df["public_assistance_households"],
            df["households"]
        ),

        # Education
        "pct_high_school": df["pct_high_school"],
        "pct_bachelors_degree": df["pct_bachelors"],
        "pct_graduate_degree": df["pct_graduate_degree"],

        # Transportation
        "pct_no_vehicle_households": df["pct_no_vehicle"],

        "pct_one_vehicle_households": safe_divide(
            df["one_vehicle_households"],
            df["households"]
        ),

        "pct_two_plus_vehicle_households": safe_divide(
            df["two_plus_vehicle_households"],
            df["households"]
        ),

        "median_commute_time": df["median_commute_time"],

        "pct_public_transit_commute": df["pct_transit_commute"],

        "pct_car_commute": safe_divide(
            df["car_commute"],
            df["workers_total"]
        ),

        "pct_walk_commute": df["pct_walk_commute"],
        "pct_bike_commute": df["pct_bike_commute"],
        "pct_work_from_home": df["pct_wfh"],

        # Housing
        "housing_units": df["housing_units"],

        "occupied_housing_units": safe_divide(
            df["occupied_units"],
            df["housing_units"]
        ),

        "vacant_housing_units": safe_divide(
            df["vacant_units"],
            df["housing_units"]
        ),

        "homeownership_rate": safe_divide(
            df["owner_occupied"],
            df["occupied_units"]
        ),

        "median_rent": df["median_rent"],
        "median_home_value": df["median_home_value"],

        "housing_density": safe_divide(
            df["housing_units"],
            df["land_area_km2"]
        ),

        "median_year_built": df["median_year_built"],

        # Land / Urban form
        "land_area_km2": df["land_area_km2"],
        "distance_to_cbd_km": df["distance_to_cbd_km"],

        # Race / Ethnicity
        "pct_white_non_hispanic": df["pct_white_non_hispanic"],
        "pct_black": df["pct_black"],
        "pct_hispanic_latino": df["pct_hispanic_latino"],
        "pct_asian": df["pct_asian"],

        "pct_other_multiracial": safe_divide(
            df["other_multiracial"],
            df["race_total"]
        ),

        # Street network features
        "intersection_density": df["intersection_density"],
        "node_density": df["node_density"],
        "street_density": df["street_density"],

        # Amenities
        "restaurant_count": df["restaurant_count"],
        "restaurant_density": df["restaurant_density"],

        "cafe_count": df["cafe_count"],
        "cafe_density": df["cafe_density"],

        "school_count": df["school_count"],
        "school_density": df["school_density"],

        "hospital_count": df["hospital_count"],
        "hospital_density": df["hospital_density"],

        "pharmacy_count": df["pharmacy_count"],
        "pharmacy_density": df["pharmacy_density"],

        "supermarket_count": df["supermarket_count"],
        "supermarket_density": df["supermarket_density"],

        "park_count": df["park_count"],
        "park_density": df["park_density"],

        "transit_stop_count": df["transit_stop_count"],
        "transit_stop_density": df["transit_stop_density"],
    })

    # TYPE CLEANUP
    float_cols = final.select_dtypes(include=["float64"]).columns
    final[float_cols] = final[float_cols].astype("float32")

    return final