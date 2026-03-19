

import pandas as pd
import numpy as np

df = pd.read_csv("dataset_binary_favor.csv")

# Keep 2000 and later
df = df[df["Year"] >= 2000].copy()

# Build grouped age variables from single year age columns
def age_cols(start, end):
    return [f"age_{float(i)}" for i in range(start, end + 1) if f"age_{float(i)}" in df.columns]

age_18_29_cols = age_cols(18, 29)
age_30_44_cols = age_cols(30, 44)
age_45_64_cols = age_cols(45, 64)
age_65_plus_cols = age_cols(65, 99)

df["age_18_29"] = df[age_18_29_cols].sum(axis=1)
df["age_30_44"] = df[age_30_44_cols].sum(axis=1)
df["age_45_64"] = df[age_45_64_cols].sum(axis=1)
df["age_65_plus"] = df[age_65_plus_cols].sum(axis=1)


# Remove columns with no variation
df = df.loc[:, df.nunique(dropna=True) > 1]

# Correlation matrix
corr_matrix = df.corr(numeric_only=True)

#filter to only include correlations abive 0.5 or below -0.5, excluding the diagonal

# correlation matrix with all variables vs nuclear favorabcolumns
nuclear_corr_matrix = corr_matrix["percent_favor"].dropna().sort_values(ascending=False)
print("Correlation matrix (filtered):")


nuclear_corr_matrix.to_csv("nuclear_favorability_correlation_matrix_all.csv")

corr_matrix = corr_matrix.where((corr_matrix.abs() > 0.5) & (corr_matrix.abs() < 1.0))


nuclear_corr_matrix = corr_matrix["percent_favor"].dropna().sort_values(ascending=False)
print("Correlation matrix (filtered):")

nuclear_corr_matrix.to_csv("nuclear_favorability_correlation_matrix_stongest.csv")
