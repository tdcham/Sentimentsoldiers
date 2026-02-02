
# %%

import pandas as pd
import os
from functools import reduce
import matplotlib.pyplot as plt



# Using year 2000 as the reference year

df = pd.read_csv("merged_nuclear_data.csv")
#df  = df[(df['Year'] >= 2000) & (df['Year'] <= 2025)]

print(df.head())

df.plot(x='Year', y='percent_oppose', kind='line', title='Percent Oppose Nuclear Energy in US Over Time')
plt.ylabel('Percent Oppose')
plt.show()


# %%

df.plot(x='Year', y='Nuclear Share of Electricity Net Generation', kind='line', title='Nuclear Share of Electricity Generation Over Time')
plt.ylabel('Nuclear Share (%)')
plt.show()

# %%
df.plot(x='Year', y='Nuclear Generating Units, Net Summer Capacity', kind='line', title='Nuclear Generating Units, Net Summer Capacity Over Time')
plt.ylabel('Net Summer Capacity (MW)')
plt.show()
# %%
df.plot(x='Year', y='Nuclear Electricity Net Generation', kind='line', title='Nuclear Electricity Net Generation Over Time')
plt.ylabel('Net Generation (MWh)')
plt.show()

# %%

df.plot(x='Year', y='Nuclear Generating Units, Total Operable Units', kind='line', title='Nuclear Generating Units, Total Operable Units Over Time')
plt.ylabel('Total Operable Units')
plt.show()

df  = df[(df['Year'] >= 1973) & (df['Year'] <= 2025)]
# %%    
