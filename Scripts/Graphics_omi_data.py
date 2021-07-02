import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime


def date_format(data):
    data["Date"] = data["Datetime"].str[0:4]+"-" + \
        data["Datetime"].str[4:6]+"-"+data["Datetime"].str[6:8]
    data["Date"] = pd.to_datetime(data["Date"])
    data.index = data["Date"]
    data = data.drop(["Date", "Datetime"], 1)
    return data


def clean_data(data, columns):
    for column in data.columns:
        if not column in columns:
            data = data.drop(column, 1)
    return data


def obtain_data_in_period(data, date_i, date_f):
    data = data[data.index >= date_i]
    data = data[data.index <= date_f]
    return data


def drop_data_useless(data, columns, limit):
    for column in columns:
        data = data[data[column] < limit]
    return data


def plot_data(data,  date_initial, date_final, path, name):
    plt.subplots(figsize=(10, 4))
    plt.subplots_adjust(top=0.963,
                        bottom=0.13,
                        left=0.062,
                        right=0.967,
                        hspace=0.2,
                        wspace=0.2)
    plt.xlabel("year")
    plt.ylabel("UV Index")
    dates, xtick = obtain_xticks(date_initial,
                                 date_final)
    plt.xlim(pd.to_datetime(date_initial).date(),
             pd.to_datetime(date_final).date())
    plt.xticks(dates, xtick)
    plt.scatter(data.index, data,
                c="#023e8a",
                marker=".")
    plt.ylim(0, 18)
    plt.yticks(np.arange(0, 20, 2))
    plt.grid(ls="--",
             color="#000000",
             alpha=0.5)
    plt.savefig("{}{}.png".format(path,
                                  name))
    plt.show()


def obtain_xticks(date_initial, date_final):
    year_i = int(date_initial[0:4])
    year_f = int(date_final[0:4])
    xtick = []
    dates = []
    for year in range(year_i, year_f+2):
        xtick.append(year)
        dates.append(pd.to_datetime("{}-01-01".format(year)))
    return dates, xtick


inputs = {
    "path data": "../Data/",
    "file data": "Data_OMI_",
    "path graphics": "../Graphics/",
    "product": "OMUVB",
    "skiprows": 50,
    "UVI limit": 20,
    "UVIcolumns": ["CSUVindex", "UVindex"],
    "file results": "UVI_",
    "day initial": "2005-01-01",
    "day final": "2019-12-31",
}
data = pd.read_fwf(inputs["path data"]+inputs["file data"]+inputs["product"]+".dat",
                   skiprows=inputs["skiprows"])
data = date_format(data)
data = clean_data(data,
                  inputs["UVIcolumns"])
data = obtain_data_in_period(data,
                             inputs["day initial"],
                             inputs["day final"])
data = drop_data_useless(data,
                         inputs["UVIcolumns"],
                         inputs["UVI limit"])
year = data[data.index.month >= 6]
year = year[year.index.month <= 7]
#print(year[year == year.max()])
print(year)
for uvicolumn in inputs["UVIcolumns"]:
    print("Creando archivo {}".format(uvicolumn))
    data_UVI = data[uvicolumn]
    plot_data(data_UVI,
              inputs["day initial"],
              inputs["day final"],
              inputs["path graphics"],
              uvicolumn)
    data_UVI.to_csv("{}{}{}.csv".format(inputs["path data"],
                                        inputs["file results"],
                                        uvicolumn),
                    float_format='%.4f')
