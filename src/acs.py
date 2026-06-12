from .acs_variables import ACS_TABLES
import pandas as pd
import censusdata

def flatten_acs_variables():
    flat = {}
    for _, variables in ACS_TABLES.items():
        flat.update(variables)

    return flat

def load_acs_data(
    state_fips,
    county_fips_list,
    year=2022,
    census_api_key=None
):

    acs_vars = flatten_acs_variables()
    variable_codes = list(acs_vars.values())
    all_tables = []

    for county in county_fips_list:
        geo = censusdata.censusgeo([
            ("state", state_fips),
            ("county", county),
            ("tract", "*")
        ])

        df = censusdata.download(
            src="acs5",
            year=year,
            geo=geo,
            var=variable_codes,
            key=census_api_key
        )

        df = df.reset_index()

        rename_map = {
            v: k for k, v in acs_vars.items()
        }

        df = df.rename(columns=rename_map)

        df["tract_id"] = df["index"].apply(
            lambda x: "".join(
                [v for _, v in x.geo]
            )
        )

        all_tables.append(df)

    acs = pd.concat(
        all_tables,
        ignore_index=True
    )

    return acs

def compute_acs_features(df):

    df = df.copy()

    # Missing ACS values
    missing_codes = [
        -666666666,
        -333333333,
        -222222222
    ]

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    for col in numeric_cols:

        df[col] = df[col].mask(
            df[col].isin(missing_codes)
        )

    # Age groups
    under_18_cols = [
        "m_under_5",
        "m_5_9",
        "m_10_14",
        "m_15_17",
        "f_under_5",
        "f_5_9",
        "f_10_14",
        "f_15_17",
    ]

    over_65_cols = [
        "m_65_66",
        "m_67_69",
        "m_70_74",
        "m_75_79",
        "m_80_84",
        "m_85_plus",
        "f_65_66",
        "f_67_69",
        "f_70_74",
        "f_75_79",
        "f_80_84",
        "f_85_plus",
    ]

    df["population_under_18"] = (
        df[under_18_cols].sum(axis=1)
    )

    df["population_over_65"] = (
        df[over_65_cols].sum(axis=1)
    )

    df["population_18_64"] = (
        df["total_population"]
        - df["population_under_18"]
        - df["population_over_65"]
    )

    # Demographic rates
    df["pct_under_18"] = (
        df["population_under_18"]
        / df["total_population"]
    )

    df["pct_18_64"] = (
        df["population_18_64"]
        / df["total_population"]
    )

    df["pct_over_65"] = (
        df["population_over_65"]
        / df["total_population"]
    )

    df["sex_ratio"] = (
        df["male_population"]
        / df["female_population"]
    )

    # Education
    df["graduate_degree"] = (
        df["masters"]
        + df["professional"]
        + df["doctorate"]
    )

    df["pct_high_school"] = (
        df["high_school"]
        / df["pop_25_plus"]
    )

    df["pct_bachelors"] = (
        df["bachelors"]
        / df["pop_25_plus"]
    )

    df["pct_graduate_degree"] = (
        df["graduate_degree"]
        / df["pop_25_plus"]
    )

    # Economics
    df["poverty_rate"] = (
        df["below_poverty"]
        / df["poverty_total"]
    )

    df["unemployment_rate"] = (
        df["unemployed"]
        / df["labor_force"]
    )

    df["employment_rate"] = (
        df["employed"]
        / df["labor_force"]
    )

    df["labor_force_participation_rate"] = (
        df["labor_force"]
        / df["total_population"]
    )

    df["snap_rate"] = (
        df["snap_households"]
        / df["households"]
    )

    # Transportation
    df["pct_no_vehicle"] = (
        df["no_vehicle_households"]
        / df["households"]
    )

    df["pct_transit_commute"] = (
        df["transit_commute"]
        / df["workers_total"]
    )

    df["pct_walk_commute"] = (
        df["walk_commute"]
        / df["workers_total"]
    )

    df["pct_bike_commute"] = (
        df["bike_commute"]
        / df["workers_total"]
    )

    df["pct_wfh"] = (
        df["wfh_commute"]
        / df["workers_total"]
    )

    # Housing
    df["vacancy_rate"] = (
        df["vacant_units"]
        / df["housing_units"]
    )

    df["homeownership_rate"] = (
        df["owner_occupied"]
        / df["occupied_units"]
    )

    # Race/Ethnicity
    race_groups = [
        "white_non_hispanic",
        "black",
        "asian",
        "hispanic_latino",
    ]

    for col in race_groups:

        df[f"pct_{col}"] = (
            df[col]
            / df["race_total"]
        )

    return df