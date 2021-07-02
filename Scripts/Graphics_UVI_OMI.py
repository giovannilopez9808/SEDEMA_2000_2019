import matplotlib.pyplot as plt
from functions import *
import pandas as pd
import numpy as np
import datetime
numyear = ["2005",
           "",
           "",
           "2008",
           "",
           "",
           "",
           "2012",
           "",
           "",
           "",
           "2016",
           "",
           "",
           "2019"]
inputs = {
    "path data": "../Data/",
    "path graphics": "../Graphics/",
    "column": "CSUVindex",
    "year initial": 2005,
    "year final": 2019,
    "UV minium": 1,
    "UV maximum": 17,
}
month_days = np.arange(0, 365, 30.5)
month_names = obtain_month_names()
UV_values = np.arange(inputs["UV minium"],
                      inputs["UV maximum"])
UVI_map = np.zeros((inputs["year final"]-inputs["year initial"]+1,
                    365))
data = pd.read_csv(inputs["path data"]+"UVI_"+inputs["column"]+".csv",
                   index_col=0)
print(inputs["column"], data.max())
data.index = pd.to_datetime(data.index)
data_mean = data.resample("MS").mean()
for year in range(inputs["year initial"], inputs["year final"]+1):
    year_i = year-inputs["year initial"]
    for day in range(365):
        date = datetime.date(year, 1, 1)+datetime.timedelta(days=day)
        try:
            value = (data[inputs["column"]][str(date)]).mean()
            UVI_map[year_i, day] = value
        except:
            month = date.month
            date = datetime.date(year, month, 1)
            value = data_mean[inputs["column"]][str(date)]
            UVI_map[year_i, day] = value
cm = colormap_UVI()
font_size = 12
print("Graficando UV Index")
fig, ax = plt.subplots(1, 1)
plt.subplots_adjust(top=0.879,
                    bottom=0.132,
                    left=0.023,
                    right=0.977,
                    hspace=0.2,
                    wspace=0.2)
year = np.arange(inputs["year final"]-inputs["year initial"]+1)
ax.set_yticks(year-0.5)
ax.set_yticklabels(numyear,
                   fontsize=font_size)
ax.set_xticks(month_days)
ax.set_xticklabels(month_names,
                   rotation=60,
                   fontsize=font_size)
map = ax.imshow(UVI_map,
                cmap=cm,
                vmin=inputs["UV minium"],
                vmax=inputs["UV maximum"],
                origin="lower")
forceAspect(ax, 1.2)
cbar = fig.colorbar(map,
                    values=UV_values+0.5,
                    ticks=UV_values)
cbar.ax.set_ylabel("UV Index",
                   rotation=-90,
                   va="bottom",
                   fontsize=11)
ax.set_title("UV Index satellite-derived in Mexico City \n Period 2005-2019")
plt.savefig("{}{}-OMI.png".format(inputs["path graphics"],
                                  inputs["column"]),
            dpi=400)
plt.show()
