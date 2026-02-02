import pandas as pd
import os
from functools import reduce


def get_path(filename, subfolder=None):
    """
    Helper to get absolute path of a file.
    If subfolder is None, it looks in the SAME folder as the script.
    """
    if subfolder:
        return os.path.join(script_dir, subfolder, filename)
    return os.path.join(script_dir, filename)


uranium_price = pd.read_csv(
    get_path("Uranium Purchase Price - Sheet1.csv"), 
    usecols=['Delivery year', 'U.S.-origin uranium (weighted-average price)', 'Foreign-origin uranium (weighted-average price)']
)

nuclear_fuel_share = pd.read_csv(
    get_path("US Nuclear Generating Statistics - Sheet1.csv"),
    usecols=['Year', 'Nuclear Fuel Share (Percent)']
)

Bisconti_data = pd.read_csv(
    get_path("Bisconti_2025_digitized_figure.csv"),
    usecols=['year', 'percent_favor', 'percent_oppose', 'percent_strongly_favor', 'percent_strongly_oppose']
)

NEI_data = pd.read_csv(
    get_path("Table_8.1_Nuclear_Energy_Overview.csv"),
    usecols=[
        'Annual Total',
        'Nuclear Generating Units, Total Operable Units',
        'Nuclear Generating Units, Net Summer Capacity',
        'Nuclear Electricity Net Generation',
        'Nuclear Share of Electricity Net Generation',
        'Nuclear Generating Units, Capacity Factor'
    ]
)

electricity_gen = pd.read_csv(
    get_path("International Energy Agency - electricity generation sources in United States.csv")
)

gallup_folder = "Gallup Data"

opinions = pd.read_csv(get_path("Gallup_OpinionsonNuclear.csv", gallup_folder))
party = pd.read_csv(get_path("Gallup_PartyIdentification.csv", gallup_folder))
alt_energy = pd.read_csv(get_path("Gallup_Alternative_vs_NonRenewable.csv", gallup_folder))
energy_access = pd.read_csv(get_path("Gallup_Availability_Afforability_Energy.csv", gallup_folder))



opinions_clean = opinions[[
    "X.1", "% Strongly/Somewhat favor", "% Strongly/Somewhat oppose"
]].rename(columns={
    "X.1": "Year",
    "% Strongly/Somewhat favor": "nuclear_support_pct",
    "% Strongly/Somewhat oppose": "nuclear_opposition_pct"
})

party_clean = party[[
    "X.1", "Republicans", "Independents", "Democrats"
]].rename(columns={
    "X.1" : "Year",
    "Republicans": "republican_nuclear_support_pct",
    "Independents": "independents_nuclear_support_pct",
    "Democrats": "democrats_nuclear_support_pct"
})

alt_energy_clean = alt_energy[[
    "X.1", "% Emphasize production of oil, gas, coal", "% Emphasize alternative energy"
]].rename(columns={
    "X.1" : "Year",
    "% Emphasize production of oil, gas, coal": "pct_prefer_nonrenewable_energy",
    "% Emphasize alternative energy": "pct_prefer_alternative_energy"
})

energy_access_clean = energy_access[[
    "X.1", "% Great deal"
]].rename(columns={
    "X.1": "Year",
    "% Great deal": "pct_concern_energy_affordability"
})

uranium_price = uranium_price.rename(columns={'Delivery year': 'Year'})

Bisconti_data = Bisconti_data.rename(columns={'year': 'Year'})
Bisconti_data = Bisconti_data[(Bisconti_data['Year'] >= 2000) & (Bisconti_data['Year'] <= 2025)]

NEI_data = NEI_data[pd.to_numeric(NEI_data['Annual Total'], errors='coerce').notna()]
NEI_data = NEI_data.rename(columns={'Annual Total': 'Year'})

nuclear = electricity_gen[electricity_gen["electricity generation sources in United States"] == "Nuclear"].copy()
nuclear = nuclear[["Year", "Value"]]
nuclear = nuclear.rename(columns={'Value': 'nuclear_generation_gwh'})



alt_energy_clean["Year"] = alt_energy_clean["Year"].astype(str).str.strip()
alt_energy_clean["Year"] = pd.to_datetime(alt_energy_clean["Year"], format='mixed').dt.year

dataframes_to_clean = [
    uranium_price, nuclear_fuel_share, opinions_clean, party_clean, 
    alt_energy_clean, energy_access_clean, nuclear, Bisconti_data, NEI_data
]

for df in dataframes_to_clean:
    df['Year'] = df['Year'].astype(int)


dfs_to_merge = [
    uranium_price, 
    nuclear_fuel_share, 
    opinions_clean, 
    party_clean, 
    alt_energy_clean, 
    energy_access_clean, 
    nuclear,
    Bisconti_data,
    NEI_data
]

def merge_on_year(left, right):
    return pd.merge(left, right, on='Year', how='outer')

final_df = reduce(merge_on_year, dfs_to_merge)
final_df = final_df.sort_values('Year').reset_index(drop=True)
print(final_df.head())
output_file = os.path.join(script_dir, "merged_nuclear_data.csv")
final_df.to_csv(output_file, index=False)
print(f"Saved to: {output_file}")
