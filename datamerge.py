import pandas as pd

# Using year 2000 as the reference year


df1 = pd.read_csv("Bisconti_2025_digitized_figure.csv")
df2 = pd.read_csv("Table_8.1_Nuclear_Energy_Overview.csv")


Bisconti_data =pd.read_csv("Bisconti_2025_digitized_figure.csv", usecols=['year', 'percent_favor','percent_oppose', 'percent_strongly_favor', 'percent_strongly_oppose'])

# Filter years 2000–2025
Bisconti_data = Bisconti_data[
    (Bisconti_data['year'] >= 2000) & (Bisconti_data['year'] <= 2025)

]
print(Bisconti_data.head())

# Gallup Data
"Gallup_Alternative_vs_NonRenewable.csv"
"Gallup_Availability_Afforability_Energy.csv"
"Gallup_OpinionsonNuclear.csv"
"Gallup_PartyIdentification.csv"

"International Energy Agency - electricity generation sources in United States.csv"
"yearly_US_only.csv"
#uranium_price = pd.read_csv("Uranium Purchase Price - Sheet1.csv", usecols=['Year', 'U.S.-origin uranium (weighted-average price)', 'Foreign-origin uranium (weighted-average price)'])
#nuclear_fuel_share = pd.read_csv("US Nuclear Generating Statistics - Sheet1.csv", usecols=['Year', 'Nuclear Fuel Share (Percent)'])
