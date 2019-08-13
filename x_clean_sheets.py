# calculate and plot expected vs. actual clean sheets,
# given full season data from x_clean_sheets.csv
# v1.0 - 13 August 2019

import pandas as pd
from scipy.stats import poisson
import numpy as np
import matplotlib.pyplot as plt

x_clean_sheets = []
xcs = 0
num_gameweeks = 38

# actual number of clean sheets for each team
clean_sheets = {
    "ARS": 8,   "BOU": 10,  "BHA": 7,   "BUR": 8,   "CAR": 10,
    "CHE": 16,  "CRY": 12,  "EVE": 14,  "FUL": 5,   "HUD": 5,
    "LEI": 10,  "LIV": 21,  "MCI": 20,  "MUN": 7,   "NEW": 11,
    "SOT": 7,   "SPU": 13,  "WAT": 7,   "WHU": 7,   "WOL": 9
}

cs = list(clean_sheets.values())
# csv contains expected clean sheets for each individual match across the season
csvfile = pd.read_csv('x_clean_sheets.csv', index_col = 0)

# calculate expected clean sheets for each team
for key in clean_sheets:
    for x in range(1, num_gameweeks + 1):
        xcs += poisson.pmf(0, csvfile[key][x])
    x_clean_sheets.append(xcs)
    xcs = 0

# plot clean sheets vs. expected clean sheets
# include line of best fit and line for cs = xcs
plt.scatter(x_clean_sheets, cs, color='b')
plt.plot(np.unique(x_clean_sheets), np.poly1d(np.polyfit(x_clean_sheets, cs, 1))
    (np.unique(x_clean_sheets)))
plt.plot([0, 22], [0, 22], 'k-', color='r')
plt.xlabel('Expected clean sheets')
plt.ylabel('Actual clean sheets')
plt.show()
