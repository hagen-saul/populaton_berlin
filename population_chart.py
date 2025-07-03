#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script for vizualization of population data of Berlin and sub-districts."""

# %% Read data files.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# TODO: Fix errors of commented files, when trying to extract specific data.
year_to_filenames = {
    2001: "EWR200112E_Matrix.csv",
    2002: "EWR200212E_Matrix.csv",
    2003: "EWR200312E_Matrix.csv",
    2004: "EWR200412E_Matrix.csv",
    2005: "EWR200512E_Matrix.csv",
    2006: "EWR200612E_Matrix.csv",
    2007: "EWR200712E_Matrix.csv",
    2008: "EWR200812E_Matrix.csv",
    2009: "EWR200912E_Matrix.csv",
    2010: "EWR201012E_Matrix.csv",
    2011: "EWR201112E_Matrix.csv",
    # 2012: "EWR201212E_Matrix.csv",
    # 2013: "EWR201312E_Matrix.csv",
    2014: "EWR201412E_Matrix.csv",
    # 2015: "EWR201512E_Matrix.csv",
    2016: "EWR201612E_Matrix.csv",
    2017: "EWR201712E_Matrix.csv",
    2018: "EWR201812E_Matrix.csv",
    2019: "EWR201912E_Matrix.csv",
    2020: "EWR202012E_Matrix.csv",
    2024: "EWR_L21_202412E_Matrix.csv",
}

year_to_data = dict()

for year, filename in year_to_filenames.items():
    population_df = pd.read_csv(filename, header=0, sep=";")
    year_to_data[year] = population_df.copy()
# print(population_df.head())

# %% Filter by PLR (Planungsregion).

# XXX: Note: Leading "0" can be ommitted, since there is an implicit
#     conversion to int when reading csv to DataFrame.
# ID of PLR "Weberwiese" prior to 2021
raum_id_weberwiese_old = 2040702
# ID of ÜPLR "Weberwiese" since 2021
raum_id_weberwiese = 2400624

year_to_population_weberwiese = dict()
for year, data in year_to_data.items():
    row = data.loc[data["RAUMID"] == raum_id_weberwiese_old]
    if row.empty:
        row = data.loc[data["RAUMID"] == raum_id_weberwiese]
    if row.empty:
        print("No data for RaumID found.")
    year_to_population_weberwiese[year] = row


# %% Filter by age and extract population data of specific region.
E_E = list()
E_0_6 = list()
E_6_12 = list()
E_12_18 = list()

column_names_0_6 = ["E_E00_01", "E_E01_02", "E_E02_03", "E_E03_05", "E_E05_06"]
column_names_6_12 = ["E_E06_07", "E_E07_08", "E_E08_10", "E_E10_12"]
column_names_12_18 = ["E_E12_14", "E_E14_15", "E_E15_18"]

# XXX: Sort by year, if file dictionary gets changed.

for year, population in year_to_population_weberwiese.items():
    try:
        E_E.append(int(population["E_E"]))
    except:
        E_E.append(0)
    E_0_6.append(int(population[column_names_0_6].sum(axis=1)))
    E_6_12.append(int(population[column_names_6_12].sum(axis=1)))
    E_12_18.append(int(population[column_names_12_18].sum(axis=1)))

print(E_E)
print(E_0_6)
print(E_6_12)
print(E_12_18)

# %% Visualization: chart of time series of total population evolution.

sns.set_theme(style="whitegrid")
population_vis = pd.DataFrame(
    list(zip(E_E)),
    year_to_population_weberwiese.keys(),
    columns=["Einwohner LOR Weberwiese"],
)
sns.lineplot(data=population_vis, palette="tab10", linewidth=2.5)
plt.show()

# %% Visualization: chart of pupil numbers in different age cohorts.

sns.set_theme(style="whitegrid")
population_vis = pd.DataFrame(
    list(zip(E_0_6, E_6_12, E_12_18)),
    year_to_population_weberwiese.keys(),
    columns=["E 0-5", "E 6-11", "E 12-18"],
)
sns.lineplot(data=population_vis, palette="tab10", linewidth=2.5)
plt.show()
