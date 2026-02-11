
import pandas as pd
import os
from functools import reduce
import matplotlib.pyplot as plt
import re


df2 = pd.read_csv("Nuclear Seniment - Support For Energy Sources.csv")

df3 = pd.read_csv("labeled_gpss.csv")
print(df2.head())


df2.columns = [c.strip() for c in df2.columns]

# extract a numeric year from the Date column
df2["Year"] = (
    df2["Date"]
    .astype(str)
    .str.extract(r"(\d{4})", expand=False)
    .astype(int)
)

# Ensure numeric percent columns
df2["Favor (%)"] = pd.to_numeric(df2["Favor (%)"], errors="coerce")
df2["Oppose (%)"] = pd.to_numeric(df2["Oppose (%)"], errors="coerce")

# Sort for clean lines
df2 = df2.sort_values(["Energy Source", "Year"])

# Pivot so each energy source becomes a line
favor_wide = df2.pivot_table(index="Year", columns="Energy Source", values="Favor (%)", aggfunc="mean")
oppose_wide = df2.pivot_table(index="Year", columns="Energy Source", values="Oppose (%)", aggfunc="mean")

# Plot Favor over time
ax = favor_wide.plot(marker="o")
ax.set_title("Percent Favor by Energy Source Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Percent Favor")
ax.legend(title="Energy Source", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.show()

# Plot Oppose over time
ax = oppose_wide.plot(marker="o")
ax.set_title("Percent Oppose by Energy Source Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Percent Oppose")
ax.legend(title="Energy Source", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.show()
