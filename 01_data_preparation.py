import pandas as pd
import numpy as np


# Step 0: Load Data

gpss = pd.read_csv("labeled_gpss.csv", low_memory=False)
nuc  = pd.read_csv("initial_merged_nuclear_data.csv", low_memory=False)

gpss.columns = gpss.columns.str.strip()
nuc.columns  = nuc.columns.str.strip()

print("GPSS columns sample:", gpss.columns.tolist()[:25])
print("Nuclear columns sample:", nuc.columns.tolist()[:25])


# Step 1: Create Year column

gpss["Year"] = pd.to_numeric(gpss["yr"], errors="coerce")
nuc["Year"]  = pd.to_numeric(nuc["Year"], errors="coerce")

gpss = gpss.dropna(subset=["Year"])
nuc  = nuc.dropna(subset=["Year"])

gpss["Year"] = gpss["Year"].astype(int)
nuc["Year"]  = nuc["Year"].astype(int)


# Step 2: Keep Relevant Columns

cols_needed = [
    "Year",
    "nucfav",
    "nucsafe",
    "favor_reduce_fossil",
    "fav_mandateC02",
    "fav_mandateC02bus",
    "fav_engylimits",
    "engy_v_envt",
    "econ_v_envt",
    "party",
    "educ",
    "age"
]

gpss = gpss[cols_needed].copy()
print("Using GPSS columns:", cols_needed)


# Step 3: Transform Qualitative to Binary / Groups


# Nuclear Favor Binary
nucfav_map = {
    "Somewhat favor": 1,
    "Strongly favor": 1,
    "Somewhat oppose": 0,
    "Strongly oppose": 0
}
gpss["nucfav_bin"] = gpss["nucfav"].map(nucfav_map)

# Nuclear Safety Binary (if present)
if "nucsafe" in gpss.columns:
    nucsafe_map = {
        "Safe": 1,
        "Very safe": 1,
        "Somewhat safe": 1,
        "Not safe": 0,
        "Unsafe": 0,
        "Somewhat unsafe": 0,
        "Very unsafe": 0
    }
    gpss["nucsafe_bin"] = gpss["nucsafe"].map(nucsafe_map)

# Policy Binary Variables
policy_vars = [
    "favor_reduce_fossil",
    "fav_mandateC02",
    "fav_mandateC02bus",
    "fav_engylimits"
]

for var in policy_vars:
    if var in gpss.columns:
        gpss[f"{var}_bin"] = gpss[var].map(nucfav_map)

# Party Grouping
party_map = {
    "Republican": "Republican",
    "Lean Republican": "Republican",
    "Democrat": "Democrat",
    "Lean Democratic": "Democrat",
    "Independent, no lean": "Independent"
}
gpss["party_group"] = gpss["party"].map(party_map)

# Education Grouping
educ_map = {
    "HS or Less": "HS_or_Less",
    "Some college": "Some_College",
    "College Grad only": "College_Grad",
    "Post-grad": "Post_Grad"
}
gpss["educ_group"] = gpss["educ"].map(educ_map)

# Age Groups
gpss["age"] = pd.to_numeric(gpss["age"], errors="coerce")
gpss["age_group"] = pd.cut(
    gpss["age"],
    bins=[17, 29, 44, 64, 120],
    labels=["18_29", "30_44", "45_64", "65_plus"]
)#may change age groups later based on distribution


# Step 4: Aggregate to Year Level


binary_cols = [c for c in gpss.columns if c.endswith("_bin")]

gpss_yearly = (
    gpss.groupby("Year")[binary_cols]
    .mean()
    .mul(100)
    .reset_index()
    .rename(columns={c: f"pct_{c}" for c in binary_cols})
)


# Step 5: Aggregate by Demographic Groups

gpss_party_yearly = (
    gpss.dropna(subset=["party_group"])
        .groupby(["Year", "party_group"])[binary_cols]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={c: f"pct_{c}" for c in binary_cols})
)

gpss_age_yearly = (
    gpss.dropna(subset=["age_group"])
        .groupby(["Year", "age_group"])[binary_cols]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={c: f"pct_{c}" for c in binary_cols})
)

gpss_educ_yearly = (
    gpss.dropna(subset=["educ_group"])
        .groupby(["Year", "educ_group"])[binary_cols]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={c: f"pct_{c}" for c in binary_cols})
)


# Step 6: Merge with Nuclear Data

final_national = nuc.merge(gpss_yearly, on="Year", how="left")
final_by_party = nuc.merge(gpss_party_yearly, on="Year", how="left")
final_by_age   = nuc.merge(gpss_age_yearly, on="Year", how="left")
final_by_educ  = nuc.merge(gpss_educ_yearly, on="Year", how="left")


# Step 7: Save Files

final_national.to_csv("final_national_dataset.csv", index=False)
final_by_party.to_csv("final_by_party_dataset.csv", index=False)
final_by_age.to_csv("final_by_age_dataset.csv", index=False)
final_by_educ.to_csv("final_by_educ_dataset.csv", index=False)

print("Saved:")
print(" - final_national_dataset.csv")
print(" - final_by_party_dataset.csv")
print(" - final_by_age_dataset.csv")
print(" - final_by_educ_dataset.csv")

print("Final national dataset columns:")
print(final_national.columns.tolist())
