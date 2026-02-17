import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILEPATH = "final_national_dataset.csv"

CORR_METHOD = "pearson"
DROP_ALL_NA_COLS = True
ONE_HOT_CATEGORICALS = False
MAX_COLS = 60

df = pd.read_csv(FILEPATH)

# ---- FILTER: 2000 and beyond ----
if "Year" in df.columns:
    df = df[df["Year"] >= 2000].copy()
else:
    print("Warning: 'Year' column not found. No filtering applied.")

# Clean up columns
if DROP_ALL_NA_COLS:
    df = df.dropna(axis=1, how="all")

# Numeric selection
if ONE_HOT_CATEGORICALS:
    df_for_corr = pd.get_dummies(df, drop_first=True)
else:
    df_for_corr = df.select_dtypes(include=[np.number]).copy()

# Limit columns if too many
if df_for_corr.shape[1] > MAX_COLS:
    keep = df_for_corr.notna().sum().sort_values(ascending=False).head(MAX_COLS).index
    df_for_corr = df_for_corr[keep]

# Correlation
corr = df_for_corr.corr(method=CORR_METHOD)

# Plot
fig_w = max(10, 0.35 * corr.shape[1])
fig_h = max(8, 0.35 * corr.shape[0])

plt.figure(figsize=(fig_w, fig_h))
im = plt.imshow(corr.values, aspect="auto", vmin=-1, vmax=1)
plt.colorbar(im, fraction=0.046, pad=0.04)

plt.xticks(range(corr.shape[1]), corr.columns, rotation=90, fontsize=8)
plt.yticks(range(corr.shape[0]), corr.index, fontsize=8)

plt.title(f"Correlation Heatmap ({CORR_METHOD}, Year ≥ 2000)")
plt.tight_layout()

out_path = "correlation_heatmap_2000plus.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Saved heatmap to: {out_path}")
print(f"Filtered to years ≥ 2000")

