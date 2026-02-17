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


import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# 1) Define Production Variables
# ---------------------------
prod_cols = [
    "nuclear_generation_gwh",
    "Nuclear Electricity Net Generation",
    "Nuclear Fuel Share (Percent)",
    "Nuclear Generating Units, Net Summer Capacity",
    "Nuclear Generating Units, Total Operable Units",
    "Nuclear Share of Electricity Net Generation"
]

prod_cols = [c for c in prod_cols if c in merged.columns]

print("Production columns used:", prod_cols)



party_sent = [
    c for c in merged.columns
    if "__Party_" in c and any(k in c.lower() for k in ["favor", "oppose", "support", "safe", "prefer"])
]

age_sent = [
    c for c in merged.columns
    if "__Age_" in c and any(k in c.lower() for k in ["favor", "oppose", "support", "safe", "prefer"])
]

educ_sent = [
    c for c in merged.columns
    if "__Educ_" in c and any(k in c.lower() for k in ["favor", "oppose", "support", "safe", "prefer"])
]

print("Party sentiment vars:", len(party_sent))
print("Age sentiment vars:", len(age_sent))
print("Education sentiment vars:", len(educ_sent))



def cross_corr_heatmap(df, row_cols, col_cols, title, out_path):

    A = df[row_cols].select_dtypes(include=[np.number]).copy()
    B = df[col_cols].select_dtypes(include=[np.number]).copy()

    # Remove constant columns
    A = A.loc[:, A.nunique(dropna=True) > 1]
    B = B.loc[:, B.nunique(dropna=True) > 1]

    # Compute cross correlation matrix
    M = np.empty((A.shape[1], B.shape[1]))

    for i, a in enumerate(A.columns):
        for j, b in enumerate(B.columns):
            M[i, j] = A[a].corr(B[b], method="pearson")

    fig_w = max(8, 0.4 * B.shape[1])
    fig_h = max(6, 0.4 * A.shape[1])

    plt.figure(figsize=(fig_w, fig_h))
    im = plt.imshow(M, aspect="auto", vmin=-1, vmax=1)
    plt.colorbar(im)

    plt.xticks(range(B.shape[1]), B.columns, rotation=90, fontsize=8)
    plt.yticks(range(A.shape[1]), A.columns, fontsize=8)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved: {out_path}")
    print(f"Rows: {A.shape[1]}, Columns: {B.shape[1]}")




cross_corr_heatmap(
    merged,
    party_sent,
    prod_cols,
    f"Party Sentiment vs Nuclear Production (Year ≥ {YEAR_CUTOFF})",
    "party_vs_production.png"
)

cross_corr_heatmap(
    merged,
    age_sent,
    prod_cols,
    f"Age Sentiment vs Nuclear Production (Year ≥ {YEAR_CUTOFF})",
    "age_vs_production.png"
)

cross_corr_heatmap(
    merged,
    educ_sent,
    prod_cols,
    f"Education Sentiment vs Nuclear Production (Year ≥ {YEAR_CUTOFF})",
    "education_vs_production.png"
)
