import matplotlib.pyplot as plt
from functions import *
import pandas as pd
import datetime
import os


def obtain_xticks():
    ticks = []
    dates = []
    for year in range(2000, 2021):
        dates.append(pd.to_datetime("{}-01-01".format(year)))
        ticks.append(year)
    return ticks, dates


def obtain_header_results(year_i, year_f):
    columns = [str(year) for year in range(year_i, year_f+1)]
    return columns


def format_data(data, columns):
    data = clean_data(data,
                      inputs["columns"])
    data = date_formtat(data)
    data = drop_negative_values(data)
    return data


def clean_data(data, columns):
    for column in data:
        if not column in columns:
            data = data.drop(column, 1)
    return data


def date_formtat(data):
    data.index = pd.to_datetime(data["Date(dd:mm:yyyy)"],
                                format="%d:%m:%Y")
    data = data.drop("Date(dd:mm:yyyy)", 1)
    return data


def drop_negative_values(data):
    return data[data["AOD_340nm"] >= 0]


def obtain_daily_mean(data):
    return data.resample("D").mean()


inputs = {
    "path data": "../Data/AERONET/",
    "columns": ["Date(dd:mm:yyyy)", "AOD_340nm"],
    "path results": "../Data/",
    "file results": "AOD_CDMX.csv",
    "year initial": 2000,
    "year final": 2019
}
files = sorted(os.listdir(inputs["path data"]))
for file in files:
    # Lectura de los Data de AERONET
    data = pd.read_csv(inputs["path data"]+file,
                       skiprows=6)
    # Se eliminan columnas innecesarias y valores donde no exista medición
    data = format_data(data,
                       inputs["columns"])
    # Calcula el promedio diario
    daily_mean = obtain_daily_mean(data)
    plt.scatter(daily_mean.index, daily_mean,
                color="royalblue",
                alpha=0.5)
years, dates = obtain_xticks()
plt.ylabel("AOD$_{340nm}$")
plt.xlim(dates[0], dates[-1])
plt.ylim(0)
plt.xticks(dates, years,
           rotation=60)
plt.grid(ls="--",
         color="#000000")
plt.show()
