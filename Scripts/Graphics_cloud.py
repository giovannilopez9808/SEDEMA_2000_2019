import matplotlib.pyplot as plt
from functions import *
import pandas as pd
import numpy as np
import datetime
inputs = {
    "path data": "../Data/",
    "file data": "Cloud_factor.csv",
    "year initial": 2005,
    "year final": 2019,
    "column": "Cld. F.",
}
print("Leyendo datos de Cloud Factor")
cloud_map = np.zeros([inputs["year final"]-inputs["year initial"]+1,
                      365])
data = pd.read_csv(inputs["path data"]+inputs["file data"], index_col=0)
data.index = pd.to_datetime(data.index)
monthly_mean = data.resample("MS").mean()
month_names = obtain_month_names()
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
for year in range(inputs["year initial"], inputs["year final"]+1):
    year_i = year-inputs["year initial"]
    for day in range(365):
        date = datetime.date(year, 1, 1)+datetime.timedelta(days=day)
        try:
            value = (data[inputs["column"]][str(date)]).mean()
            cloud_map[year_i, day] = value
        except:
            month = date.month
            date = datetime.date(year, month, 1)
            value = monthly_mean[inputs["column"]][str(date)]
            cloud_map[year_i, day] = value
daysnum = np.arange(0, 365, 30.5)
year = np.arange(inputs["year final"]-inputs["year initial"]+1)
fig, ax = plt.subplots(1, 1)
plt.subplots_adjust(left=0.11,
                    right=0.97,
                    bottom=0.20,
                    top=0.94)
map = ax.imshow(cloud_map,
                interpolation="bessel",
                cmap="coolwarm",
                origin="lower")
forceAspect(ax, 1.2)
ax.set_title("Period 2005-2019",
             fontsize="large")
ax.set_yticks(year-0.5)
ax.set_yticklabels(numyear,
                   fontsize="large")
ax.set_xticks(daysnum)
ax.set_xticklabels(month_names,
                   rotation=60,
                   fontsize="large")
ax.grid(linewidth=1,
        color="black",
        linestyle="--")
cbar = fig.colorbar(map,
                    ticks=np.arange(0, 1.2, 0.2),
                    values=np.arange(0, 1.2, 0.2))
cbar.ax.set_ylabel("Cloud Factor",
                   rotation=-90,
                   va="bottom",
                   fontsize="large")
plt.show()
#plt.savefig("../Graficas/CloudDaily.png", dpi=200)
