import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Paths
NATIONAL_PATH = "final_national_dataset.csv"
PARTY_PATH    = "final_by_party_dataset.csv"
AGE_PATH      = "final_by_age_dataset.csv"
EDUC_PATH     = "final_by_educ_dataset.csv"

# Options
YEAR_CUTOFF = 2000
CORR_METHOD = "pearson"
MAX_COLS = 80  # reduce if labels get too crowded

def find_first_existing_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def pivot_group_wide(df, year_col="Year", group_col=None, prefix=None):
    """
    Converts a long subgroup table into a wide table:
    rows: Year
    columns: numeric_variable__GroupValue
    """
    if group_col is None:
        raise ValueError("group_col is required for pivot_group_wide")

    if prefix is None:
        prefix = group_col

    df = df.copy()

    # keep numeric columns only (besides year and group)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != year_col]

    if len(numeric_cols) == 0:
        raise ValueError(f"No numeric columns found to pivot in dataset with group_col={group_col}")

    # build wide tables per variable, then merge them
    wide_parts = []
    for var in numeric_cols:
        tmp = df.pivot_table(index=year_col, columns=group_col, values=var, aggfunc="mean")

        # rename columns to var__Group
        tmp.columns = [f"{var}__{prefix}_{str(g)}" for g in tmp.columns]
        wide_parts.append(tmp)

    wide = pd.concat(wide_parts, axis=1).reset_index()
    return wide

# 1) Load datasets
national = pd.read_csv(NATIONAL_PATH)
party    = pd.read_csv(PARTY_PATH)
age      = pd.read_csv(AGE_PATH)
educ     = pd.read_csv(EDUC_PATH)

# 2) Filter Year >= 2000
for name, df in [("national", national), ("party", party), ("age", age), ("educ", educ)]:
    if "Year" not in df.columns:
        raise ValueError(f"{name} dataset is missing a 'Year' column")
    df = df[df["Year"] >= YEAR_CUTOFF].copy()
    if name == "national": national = df
    if name == "party": party = df
    if name == "age": age = df
    if name == "educ": educ = df

# 3) Detect group columns and pivot wide
party_group = find_first_existing_col(party, ["party_group", "Party", "PARTY", "partisan", "Partisan"])
age_group   = find_first_existing_col(age,   ["age_group", "AgeGroup", "age", "Age", "AGE", "group", "Group"])
educ_group  = find_first_existing_col(educ,  ["educ_group", "Educ", "education", "Education", "EDUC", "group", "Group"])

if party_group is None:
    raise ValueError("Could not find a party group column in the party dataset")
if age_group is None:
    raise ValueError("Could not find an age group column in the age dataset")
if educ_group is None:
    raise ValueError("Could not find an education group column in the education dataset")

party_wide = pivot_group_wide(party, year_col="Year", group_col=party_group, prefix="Party")
age_wide   = pivot_group_wide(age,   year_col="Year", group_col=age_group,   prefix="Age")
educ_wide  = pivot_group_wide(educ,  year_col="Year", group_col=educ_group,  prefix="Educ")

# 4) Keep only numeric columns in national (plus Year)
national_num = national[["Year"] + national.select_dtypes(include=[np.number]).columns.tolist()].copy()
national_num = national_num.loc[:, ~national_num.columns.duplicated()]

# 5) Merge everything on Year
merged = national_num.merge(party_wide, on="Year", how="left") \
                     .merge(age_wide,   on="Year", how="left") \
                     .merge(educ_wide,  on="Year", how="left")

# 6) Correlation on numeric columns
df_for_corr = merged.select_dtypes(include=[np.number]).copy()

# Optional: limit columns if too many
if df_for_corr.shape[1] > MAX_COLS:
    keep = df_for_corr.notna().sum().sort_values(ascending=False).head(MAX_COLS).index
    df_for_corr = df_for_corr[keep]

corr = df_for_corr.corr(method=CORR_METHOD)

# 7) Plot heatmap
fig_w = max(12, 0.35 * corr.shape[1])
fig_h = max(10, 0.35 * corr.shape[0])

plt.figure(figsize=(fig_w, fig_h))
im = plt.imshow(corr.values, aspect="auto", vmin=-1, vmax=1)
plt.colorbar(im, fraction=0.046, pad=0.04)

plt.xticks(range(corr.shape[1]), corr.columns, rotation=90, fontsize=7)
plt.yticks(range(corr.shape[0]), corr.index, fontsize=7)

plt.title(f"Correlation Heatmap with Subgroups (Year >= {YEAR_CUTOFF}, {CORR_METHOD})")
plt.tight_layout()

out_path = "correlation_heatmap_all_sources_2000plus.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Saved heatmap to: {out_path}")
print(f"Merged shape: {merged.shape}")
print(f"Columns used in corr: {df_for_corr.shape[1]}")
