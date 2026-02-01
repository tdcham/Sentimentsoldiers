import pandas as pd

# Read Bisconti sentiment data
Bisconti_data = pd.read_csv(
    "Bisconti_2025_digitized_figure.csv",
    usecols=['year', 'percent_favor', 'percent_oppose',
             'percent_strongly_favor', 'percent_strongly_oppose']
)

# Filter years 2000–2025
Bisconti_data = Bisconti_data[
    (Bisconti_data['year'] >= 2000) & (Bisconti_data['year'] <= 2025)
]

print(Bisconti_data.head())


# Read nuclear energy data (NEI)
NEI_data = pd.read_csv(
    "Table_8.1_Nuclear_Energy_Overview.csv",
    usecols=[
        'Annual Total',
        'Nuclear Generating Units, Total Operable Units',
        'Nuclear Generating Units, Net Summer Capacity',
        'Nuclear Electricity Net Generation',
        'Nuclear Share of Electricity Net Generation',
        'Nuclear Generating Units, Capacity Factor'
    ]
)
NEI_data = NEI_data[pd.to_numeric(NEI_data['Annual Total'], errors='coerce').notna()]
NEI_data['Annual Total'] = NEI_data['Annual Total'].astype(int)


# Filter years 2000–2025
NEI_data = NEI_data[
    (NEI_data['Annual Total'] >= 2000) & 
    (NEI_data['Annual Total'] <= 2025)
]

print(NEI_data.head())


# Gallup Data
"Gallup_Alternative_vs_NonRenewable.csv"
"Gallup_Availability_Afforability_Energy.csv"
"Gallup_OpinionsonNuclear.csv"
"Gallup_PartyIdentification.csv"

"International Energy Agency - electricity generation sources in United States.csv"
"yearly_US_only.csv"
#uranium_price = pd.read_csv("Uranium Purchase Price - Sheet1.csv", usecols=['Year', 'U.S.-origin uranium (weighted-average price)', 'Foreign-origin uranium (weighted-average price)'])
#nuclear_fuel_share = pd.read_csv("US Nuclear Generating Statistics - Sheet1.csv", usecols=['Year', 'Nuclear Fuel Share (Percent)'])
