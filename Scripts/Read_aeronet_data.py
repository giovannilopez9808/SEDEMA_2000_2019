from functions import *
import pandas as pd
import datetime
import os


def obtain_index_results():
    days = obtain_days_of_the_year(2019)
    index = []
    for day in range(days):
        date = conseday_to_date(day, 2019)
        date = str(date)[5:10]
        index.append(date)
    return index


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


def obtain_days_of_the_year(year):
    date_i = datetime.date(year, 1, 1)
    date_f = datetime.date(year, 12, 31)
    days = (date_f-date_i).days
    return days


def write_results(year, data):
    print("{}\t{:.2f}".format(year, data))


inputs = {
    "path data": "../Data/AERONET/",
    "columns": ["Date(dd:mm:yyyy)", "AOD_340nm"],
    "path results": "../Data/",
    "file results": "AOD_CDMX.csv",
    "year initial": 2000,
    "year final": 2019
}
files = sorted(os.listdir(inputs["path data"]))
index = obtain_index_results()
columns = obtain_header_results(inputs["year initial"],
                                inputs["year final"])
results = pd.DataFrame(index=index,
                       columns=columns,)
for file in files:
    year, _ = file.split(".")
    # Obtiene el numero de dias en el año
    days = obtain_days_of_the_year(int(year))
    # Lectura de los Data de AERONET
    data = pd.read_csv(inputs["path data"]+file,
                       skiprows=6)
    # Se eliminan columnas innecesarias y valores donde no exista medición
    data = format_data(data,
                       inputs["columns"])
    # Calcula el promedio diario
    daily_mean = obtain_daily_mean(data)
    daily_mean.index = daily_mean.index.astype(str).str[5:10]
    results[year] = daily_mean["AOD_340nm"]
results.to_csv("{}{}".format(inputs["path results"],
                             inputs["file results"]),
               float_format="%.3f")
