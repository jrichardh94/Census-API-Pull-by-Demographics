import sys
import requests
import pandas as pd

API_KEY = "REDACTED"

BASE_URL = "https://api.census.gov/data/2024/acs/acs5"

if len(sys.argv) > 1:
    STATE_FIPS = sys.argv[1]
else:
    raise ValueError("Please provide a STATE_FIPS (e.g., 13 for Georgia)")

# ==========================================================
# 🔹 FUNCTION: CALL CENSUS API
# ==========================================================
def get_acs_data(params):
    response = requests.get(BASE_URL, params=params)
    
    print("Status:", response.status_code)
    
    if response.status_code != 200:
        print(response.text)
        raise Exception("API request failed")
    
    data = response.json()
    return pd.DataFrame(data[1:], columns=data[0])


# ==========================================================
# 🔹 1. TOTAL POPULATION + AGE (B01001)
# ==========================================================
params_total = {
    "get": "NAME,B01001_001E,"
           "B01001_007E,B01001_008E,B01001_009E,B01001_010E,B01001_011E,"
           "B01001_012E,B01001_013E,B01001_014E,"
           "B01001_015E,B01001_016E,B01001_017E,B01001_018E,B01001_019E,"
           "B01001_020E,B01001_021E,B01001_022E,B01001_023E,B01001_024E,B01001_025E,"
           "B01001_031E,B01001_032E,B01001_033E,B01001_034E,B01001_035E,"
           "B01001_036E,B01001_037E,B01001_038E,"
           "B01001_039E,B01001_040E,B01001_041E,B01001_042E,B01001_043E,"
           "B01001_044E,B01001_045E,B01001_046E,B01001_047E,B01001_048E,B01001_049E",
    "for": "county:*",
    "in": f"state:{STATE_FIPS}",
    "key": API_KEY
}

df_total = get_acs_data(params_total)

# Convert everything EXCEPT known string columns
cols_total = [col for col in df_total.columns if col not in ["NAME", "state", "county"]]

df_total[cols_total] = df_total[cols_total].apply(pd.to_numeric)


# ==========================================================
# 🔹 2. BLACK AGE (B01001B)
# ==========================================================
params_black = {
    "get": "NAME,"
           "B01001B_007E,B01001B_008E,B01001B_009E,"
           "B01001B_010E,B01001B_011E,"
           "B01001B_012E,B01001B_013E,"
           "B01001B_014E,B01001B_015E,B01001B_016E,"
           "B01001B_022E,B01001B_023E,B01001B_024E,"
           "B01001B_025E,B01001B_026E,"
           "B01001B_027E,B01001B_028E,"
           "B01001B_029E,B01001B_030E,B01001B_031E",
    "for": "county:*",
    "in": f"state:{STATE_FIPS}",
    "key": API_KEY
}

df_black = get_acs_data(params_black)
df_black = df_black.drop(columns=["NAME"])

cols_black = [col for col in df_black.columns if col not in ["NAME", "state", "county"]]
df_black[cols_black] = df_black[cols_black].apply(pd.to_numeric)


# ==========================================================
# 🔹 3. RACE TOTALS (B02001)
# ==========================================================
params_race = {
    "get": "NAME,B02001_002E,B02001_003E,B02001_005E",
    "for": "county:*",
    "in": f"state:{STATE_FIPS}",
    "key": API_KEY
}

df_race = get_acs_data(params_race)
df_race = df_race.drop(columns=["NAME"])

cols_race = [col for col in df_race.columns if col not in ["NAME", "state", "county"]]
df_race[cols_race] = df_race[cols_race].apply(pd.to_numeric)


# ==========================================================
# 🔹 4. INCOME (B19001)
# ==========================================================
params_income = {
    "get": "NAME,"
           "B19001_002E,B19001_003E,B19001_004E,B19001_005E,"  # low income
           "B19001_014E,B19001_015E,B19001_016E,B19001_017E",  # high income
    "for": "county:*",
    "in": f"state:{STATE_FIPS}",
    "key": API_KEY
}

df_income = get_acs_data(params_income)
df_income = df_income.drop(columns=["NAME"])

cols_income = [col for col in df_income.columns if col not in ["NAME", "state", "county"]]
df_income[cols_income] = df_income[cols_income].apply(pd.to_numeric)


# ==========================================================
# 🔹 5. MERGE ALL TABLES
# ==========================================================
df = df_total.merge(df_black, on=["state", "county"])
df = df.merge(df_race, on=["state", "county"])
df = df.merge(df_income, on=["state", "county"])

# ==========================================================
# 🔹 6. CREATE GEOID + COUNTY NAME
# ==========================================================
df["geoid"] = df["state"] + df["county"]
df[["county_name", "state_name"]] = df["NAME"].str.split(", ", expand=True)
state_name = df["state_name"].iloc[0]
state_name_clean = state_name.lower().replace(" ", "_")


# ==========================================================
# 🔹 7. CREATE AGE BUCKETS (TOTAL)
# ==========================================================
df["total_18_29"] = df[[
    "B01001_007E","B01001_008E","B01001_009E","B01001_010E","B01001_011E",
    "B01001_031E","B01001_032E","B01001_033E","B01001_034E","B01001_035E"
]].sum(axis=1)

df["total_30_44"] = df[[
    "B01001_012E","B01001_013E","B01001_014E",
    "B01001_036E","B01001_037E","B01001_038E"
]].sum(axis=1)

df["total_45_64"] = df[[
    "B01001_015E","B01001_016E","B01001_017E","B01001_018E","B01001_019E",
    "B01001_039E","B01001_040E","B01001_041E","B01001_042E","B01001_043E"
]].sum(axis=1)

df["total_65_plus"] = df[[
    "B01001_020E","B01001_021E","B01001_022E","B01001_023E","B01001_024E","B01001_025E",
    "B01001_044E","B01001_045E","B01001_046E","B01001_047E","B01001_048E","B01001_049E"
]].sum(axis=1)


# ==========================================================
# 🔹 8. CREATE BLACK AGE BUCKETS
# ==========================================================
df["black_18_29"] = df[[
    "B01001B_007E","B01001B_008E","B01001B_009E",
    "B01001B_022E","B01001B_023E","B01001B_024E"
]].sum(axis=1)

df["black_30_44"] = df[[
    "B01001B_010E","B01001B_011E",
    "B01001B_025E","B01001B_026E"
]].sum(axis=1)

df["black_45_64"] = df[[
    "B01001B_012E","B01001B_013E",
    "B01001B_027E","B01001B_028E"
]].sum(axis=1)

df["black_65_plus"] = df[[
    "B01001B_014E","B01001B_015E","B01001B_016E",
    "B01001B_029E","B01001B_030E","B01001B_031E"
]].sum(axis=1)


# ==========================================================
# 🔹 9. INCOME BUCKETS
# ==========================================================
df["low_income_hh"] = df[[
    "B19001_002E","B19001_003E","B19001_004E","B19001_005E"
]].sum(axis=1)

df["high_income_hh"] = df[[
    "B19001_014E","B19001_015E","B19001_016E","B19001_017E"
]].sum(axis=1)


# ==========================================================
# 🔹 10. FINAL OUTPUT
# ==========================================================
df_final = df[[
    "geoid",
    "county_name",
    "B01001_001E",
    "total_18_29",
    "total_30_44",
    "total_45_64",
    "total_65_plus",
    "black_18_29",
    "black_30_44",
    "black_45_64",
    "black_65_plus",
    "B02001_002E",
    "B02001_003E",
    "B02001_005E",
    "low_income_hh",
    "high_income_hh"
]]

df_final = df_final.rename(columns={
    "B01001_001E": "total_pop",
    "B02001_002E": "white_pop",
    "B02001_003E": "black_pop",
    "B02001_005E": "asian_pop"
})

print(df_final.head())

filename = f"{STATE_FIPS}_{state_name_clean}_demographics.csv"
df_final.to_csv(filename, index=False)