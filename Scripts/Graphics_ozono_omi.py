import matplotlib.pyplot as plt
from functions import *
import pandas as pd
import numpy as np
import datetime


def read_data(path, name):
    data = pd.read_csv(inputs["path data"]+inputs["file data"],
                       index_col=0)
    data.index = pd.to_datetime(data.index,
                                format="%m-%d")
    data_monthly_mean = obtain_monthly_mean(data)
    data = data.fillna(-1)
    return data, data_monthly_mean


def obtain_monthly_mean(data):
    return data.resample("MS").mean()


def write_data_on_matrix(data, data_monthly_mean, year_i, year_f):
    data_matrix = np.zeros((year_f-year_i+1, 365))
    for day, date in enumerate(data.index):
        for year in range(year_i, year_f+1):
            value = data[str(year)][date]
            if value != -1:
                data_matrix[year-year_i, day] = value
            else:
                date_month = pd.to_datetime(
                    "1900-{}-01".format(str(date.month).zfill(2)))
                data_matrix[year-year_i,
                            day] = data_monthly_mean[str(year)][date_month]
    return data_matrix


def define_yticks(ax, year_initial, year_final):
    years_number, years = obtain_yticks(year_initial, year_final)
    ax.set_yticks(years_number)
    ax.set_yticklabels(years)


def obtain_yticks(year_initial, year_final):
    years = np.arange(year_initial, year_final+1)
    years_number = years-year_initial-0.5
    return years_number, years


def define_xticks(ax):
    month_days, month_names = obtain_xticks()
    ax.set_xticks(month_days)
    ax.set_xticklabels(month_names)


def obtain_xticks():
    month_names = obtain_month_names()
    month_days = obtain_month_days()
    return month_days, month_names


def obtain_month_days():
    month_days = []
    for month in range(1, 13):
        day = (datetime.date(2019, month, 1) -
               datetime.date(2019, 1, 1)).days
        month_days.append(day)
    return month_days


inputs = {
    "path data": "../Data/",
    "file data": "O3_OMI.csv",
    "path graphics": "../Graphics/",
    "graphic name": "O3",
    "map color": "viridis",
    "year initial": 2005,
    "year final": 2019
}
data, data_monthly_mean = read_data(inputs["path data"],
                                    inputs["file data"])
data_matrix = write_data_on_matrix(data,
                                   data_monthly_mean,
                                   inputs["year initial"],
                                   inputs["year final"])
fig, ax = plt.subplots()
plt.subplots_adjust(top=0.922,
                    bottom=0.081,
                    left=0.023,
                    right=0.977,
                    hspace=0.2,
                    wspace=0.2)
plt.title("Period 2005-2019",
          fontsize="large")
define_xticks(ax)
define_yticks(ax,
              inputs["year initial"],
              inputs["year final"],)
ax.grid(linewidth=1,
        color="#000000",
        linestyle="--")
levels = np.arange(200,
                   340,
                   20)
map_data = ax.imshow(data_matrix,
                     cmap=inputs["map color"],
                     origin="lower",
                     )
cbar = fig.colorbar(map_data,
                    values=np.delete(levels+10, -1),
                    ticks=levels,
                    )
cbar.ax.set_ylabel("Total Ozone Column (DU)",
                   rotation=-90,
                   va="bottom",
                   fontsize="large")
cbar.set_ticklabels(np.array(levels, dtype=str))
forceAspect(ax,
            1)
# <---------Guardado de la grafica---------->
plt.savefig(inputs["path graphics"]+inputs["graphic name"],
            dpi=400)
