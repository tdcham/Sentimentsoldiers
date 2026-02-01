import pandas as pd

# Using year 2000 as the reference year

"Sentimentsoldiers/Bisconti_2025_digitized_figure.csv"

uranium_price = pd.read_csv("SentimentSoldiers/Uranium Purchace Price - Sheet1.csv", usecols=['Year', 'U.S.-origin uranium (weighted-average price)', 'Foreign-origin uranium (weighted-average price)'])
nuclear_fuel_share = pd.read_csv("SentimentSoldiers/US Nuclear Generating Statistics - Sheet1.csv", usecols=['Year', 'Nuclear Fuel Share (Percent)'])