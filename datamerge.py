import pandas as pd

# Using year 2000 as the reference year

"Sentimentsoldiers/Bisconti_2025_digitized_figure.csv"


# Gallup Data
"Gallup_Alternative_vs_NonRenewable.csv"
"Gallup_Availability_Afforability_Energy.csv"
"Gallup_OpinionsonNuclear.csv"
"Gallup_PartyIdentification.csv"

"International Energy Agency - electricity generation sources in United States.csv"
"yearly_US_only.csv"

opinions = pd.read_csv("Gallup Data/Gallup_OpinionsonNuclear.csv")
party = pd.read_csv("Gallup Data/Gallup_PartyIdentification.csv")
alt_energy = pd.read_csv("Gallup Data/Gallup_Alternative_vs_NonRenewable.csv")
energy_access = pd.read_csv("Gallup Data/Gallup_Availability_Afforability_Energy.csv")

opinions_clean = opinions[[
    "X.1",
    "% Strongly/Somewhat favor",
    "% Strongly/Somewhat oppose"
]].rename(columns={
    "X.1": "Year",
    "% Strongly/Somewhat favor": "nuclear_support_pct",
    "% Strongly/Somewhat oppose": "nuclear_opposition_pct"
})
print(opinions_clean.head())

party_clean = party[[
    "X.1",
    "Republicans",
    "Independents",
    "Democrats"
]].rename(columns={
    "X.1" : "Year",
    "Republicans": "republican_nuclear_support_pct",
    "Independents": "independents_nuclear_support_pct",
    "Democrats": "democrats_nuclear_support_pct"
})

alt_energy_clean = alt_energy[[
    "X.1",
    "% Emphasize production of oil, gas, coal",
    "% Emphasize alternative energy"
]].rename(columns={
    "X.1" : "Year",
    "% Emphasize production of oil, gas, coal": "pct_prefer_nonrenewable_energy",
    "% Emphasize alternative energy": "pct_prefer_alternative_energy"
})
print(alt_energy_clean.head())

energy_access_clean = energy_access[[
    "X.1",
    "% Great deal"
]].rename(columns={
    "X.1": "Year",
    "% Great deal": "pct_concern_energy_affordability"
})

print(energy_access_clean.head())
print(alt_energy_clean.head())
print(party_clean.head())
print(opinions_clean.head())

#electricity_gen = pd.read_csv("Sentimentsoldiers/International Energy Agency - electricity generation sources in United States.csv")
#us_nuclear_gen_stat = pd.read_csv("Sentimentsoldiers/yearly_US_only.csv")

electricity_gen = pd.read_csv("International Energy Agency - electricity generation sources in United States.csv")
print(electricity_gen.head())

nuclear = electricity_gen[electricity_gen["electricity generation sources in United States"] == "Nuclear"].copy()
nuclear = nuclear[["Year", "Value"]]
#nuclear["value"] = pd.to_numeric(nuclear["value"], errors="coerce")
print(nuclear.head())



#uranium_price = pd.read_csv("SentimentSoldiers/Uranium Purchace Price - Sheet1.csv", usecols=['Year', 'U.S.-origin uranium (weighted-average price)', 'Foreign-origin uranium (weighted-average price)'])
#nuclear_fuel_share = pd.read_csv("SentimentSoldiers/US Nuclear Generating Statistics - Sheet1.csv", usecols=['Year', 'Nuclear Fuel Share (Percent)'])

