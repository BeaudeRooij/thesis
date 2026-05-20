ACS_TABLES = {
    "demographics": {

        # population
        "total_population": "B01003_001E",

        # age
        "median_age": "B01002_001E",

        # sex
        "male_population": "B01001_002E",
        "female_population": "B01001_026E",

        # households
        "households": "B11001_001E",
        "avg_household_size": "B25010_001E",

        # UNDER 18
        "m_under_5": "B01001_003E",
        "m_5_9": "B01001_004E",
        "m_10_14": "B01001_005E",
        "m_15_17": "B01001_006E",

        "f_under_5": "B01001_027E",
        "f_5_9": "B01001_028E",
        "f_10_14": "B01001_029E",
        "f_15_17": "B01001_030E",

        # 65+
        "m_65_66": "B01001_020E",
        "m_67_69": "B01001_021E",
        "m_70_74": "B01001_022E",
        "m_75_79": "B01001_023E",
        "m_80_84": "B01001_024E",
        "m_85_plus": "B01001_025E",

        "f_65_66": "B01001_044E",
        "f_67_69": "B01001_045E",
        "f_70_74": "B01001_046E",
        "f_75_79": "B01001_047E",
        "f_80_84": "B01001_048E",
        "f_85_plus": "B01001_049E",
    },

    "socioeconomic": {

        "median_income": "B19013_001E",

        "per_capita_income": "B19301_001E",

        "poverty_total": "B17001_001E",
        "below_poverty": "B17001_002E",

        "labor_force": "B23025_003E",
        "employed": "B23025_004E",
        "unemployed": "B23025_005E",

        "snap_households": "B22010_002E",

        "public_assistance_households": "B19057_002E",
    },

    "education": {

        "high_school": "B15003_017E",

        "bachelors": "B15003_022E",

        "masters": "B15003_023E",

        "professional": "B15003_024E",

        "doctorate": "B15003_025E",

        "pop_25_plus": "B15003_001E",
    },

    "transportation": {

        # commute mode
        "workers_total": "B08301_001E",

        "car_commute": "B08301_003E",

        "transit_commute": "B08301_010E",

        "bike_commute": "B08301_018E",

        "walk_commute": "B08301_019E",

        "wfh_commute": "B08301_021E",

        # commute time
        "median_commute_time": "B08303_001E",

        # vehicle ownership
        "no_vehicle_households": "B08201_002E",

        "one_vehicle_households": "B08201_003E",

        "two_vehicle_households": "B08201_004E",

        "three_plus_vehicle_households": "B08201_005E",
    },

    "housing": {

        "housing_units": "B25001_001E",

        "occupied_units": "B25002_002E",

        "vacant_units": "B25002_003E",

        "owner_occupied": "B25003_002E",

        "renter_occupied": "B25003_003E",

        "median_rent": "B25064_001E",

        "median_home_value": "B25077_001E",

        "median_year_built": "B25035_001E",
    },

    "race_ethnicity": {

        "race_total": "B03002_001E",

        "white_non_hispanic": "B03002_003E",

        "black": "B03002_004E",

        "asian": "B03002_006E",

        "hispanic_latino": "B03002_012E",
    }
}