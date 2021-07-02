import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os


def format_data(data, resize):
    data.index = pd.to_datetime(data["Dates"])
    data = data.drop(["Dates", "parameter", "unit"], 1)
    data["value"] = data["value"]*resize*40
    return data


colors = {
    "CHO": "Blue",
    "CUA": "#03071e",
    "CUT": "#83c5be",
    "FAC":  "#d00000",
    "HAN": "#b07d62",
    "LAA": "#f72585",
    "MER": "black",
    "MON": "Purple",
    "MPA": "#0096c7",
    "PED": "#f89edf",
    "SAG": "orange",
    "SFE": "Green",
    "TLA": "cyan",
}
for month in range(1, 13):
    inputs = {
        "path data": "../Data/SEDEMA_Data/Radiation/",
        "path stations": "../Stations/",
        "path graphics": "../Graphics/Daily_maximum/",
        "radiation": "UVB",
        "size": 0.0583,
        "year": "2019",
        "day initial": "2019-"+str(month).zfill(2)+"-01",
        "day final": "2019-"+str(month+1).zfill(2)+"-01",

    }
    if month == 12:
        inputs["day final"] = "2019-12-31"
    file = inputs["radiation"]+"_"+inputs["year"]+".csv"
    stations = sorted(os.listdir(inputs["path stations"]))
    data = pd.read_csv(inputs["path data"]+file)
    data = format_data(data,
                       inputs["size"])
    index = data.resample("D").max()
    daily_max = pd.DataFrame(columns=stations,
                             index=index.index)
    for station in stations:
        data_max = data[data["cve_station"] == station]
        data_max = data_max[data_max.index.hour >= 11]
        data_max = data_max[data_max.index.hour <= 15]
        data_max = data_max.resample("D").max()
        daily_max[station] = data_max["value"]
    data_max = daily_max[daily_max.index <= inputs["day final"]]
    data_max = data_max[data_max.index >= inputs["day initial"]]
    for station in stations:
        data = data_max[station]
        if data.count() != 0:
            plt.plot(data,
                     label=station,
                     ls="--",
                     marker="o",
                     color=colors[station])
    plt.legend(ncol=5,
               frameon=False,
               fontsize=9,
               bbox_to_anchor=(0.9, 1.05, 0, 0.1))
    plt.ylim(2, 16)
    plt.xlim(pd.to_datetime(inputs["day initial"]),
             pd.to_datetime(inputs["day final"]))
    plt.yticks([i for i in range(2, 17)])
    plt.grid(ls="--",
             color="#000000",
             alpha=0.5)
    plt.xticks(rotation=60)
    plt.ylabel("UV Index")
    plt.subplots_adjust(top=0.881,
                        bottom=0.211,
                        left=0.097,
                        right=0.936,
                        hspace=0.2,
                        wspace=0.2,
                        )
    plt.savefig(inputs["path graphics"]+"{}.png".format(month))
    plt.clf()
