import numpy as np
import matplotlib.pyplot as plt
import os
parameters = {
    "path stations": "../Data/Stations/",
    "path graphics": "../Graphics/",
    "graphics name": "season",
    "fontsize ticks": 16,
    "fontsize legend": 14,
    "dates": {"180420": "20 April 2018",
              "170623": "23 June 2017",
              "171113": "13 November 2017",
              "180202": "02 February 2018"},
    "colors": {"CHO": "Blue",
               "CUA": "#03071e",
               "CUT": "#6a040f",
               "FAC":  "#d00000",
               "HAN": "#b07d62",
               "LAA": "#7400b8",
               "MER": "black",
               "MON": "Purple",
               "MPA": "#0096c7",
               "PED": "#f89edf",
               "SAG": "orange",
               "SFE": "Green",
               "TLA": "cyan",
               }
}
dir_stations = parameters["path stations"]
stations = sorted(os.listdir(dir_stations))
fig, axs = plt.subplots(2, 2,
                        figsize=(12, 9))
axs = np.reshape(axs, 4)
for date, ax in zip(parameters["dates"], axs):
    title = parameters["dates"][date]
    if ax in [axs[0], axs[2]]:
        ax.set_ylabel("UV Index",
                      fontsize=parameters["fontsize ticks"])
    if ax in [axs[2], axs[-1]]:
        ax.set_xlabel("CST (UTC - 6h)",
                      fontsize=parameters["fontsize ticks"])
    ax.set_title(title,
                 fontsize=parameters["fontsize ticks"])
    ax.set_ylim(0, 15)
    ax.set_yticks(np.arange(0, 15+3, 3))
    ax.set_xlim(6, 20)
    ax.set_xticks(np.arange(6, 19+2, 2))
    ax.tick_params(labelsize=parameters["fontsize ticks"])
    for station in stations:
        color = parameters["colors"][station]
        path_data = "{}{}/Measurements/".format(dir_stations,
                                                station)
        hour, data = np.loadtxt("{}{}Ery.csv".format(path_data,
                                                     date),
                                unpack=True,
                                delimiter=",")
        if(np.mean(data) != 0):
            data = data*40
            ax.plot(hour, data,
                    label=station,
                    c=color,
                    marker=".",
                    ls="none",
                    ms=3,
                    alpha=0.7)
    ax.legend(ncol=5,
              labelspacing=0.25,
              borderaxespad=0.25,
              handletextpad=0.2,
              mode="expand",
              loc="upper left",
              markerscale=4,
              scatterpoints=1,
              frameon=False,
              fontsize=parameters["fontsize legend"])
plt.subplots_adjust(left=0.079,
                    bottom=0.09,
                    right=0.955,
                    top=0.921,
                    wspace=0.155,
                    hspace=0.2)
plt.savefig("{}{}.png".format(parameters["path graphics"],
                              parameters["graphics name"]),
            dpi=400)
