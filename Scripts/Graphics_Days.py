import matplotlib.pyplot as plt
import numpy as np
import os

inputs = {
    "path stations": "../Stations/",
    "date": "190803",
}
colors = {
    "CHO": "Blue",
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
    "TLA": "#52b788",
}
stations = sorted(os.listdir(inputs["path stations"]))
for station in stations:
    path = inputs["path stations"]+station+"/Erythemal/"
    try:
        hour, data = np.loadtxt(path+inputs["date"]+".txt",
                                unpack=True)
        if np.mean(data) != 0:
            color = colors[station]
            plt.plot(hour, data*40,
                     label=station,
                     marker="o",
                     color=color)
    except:
        pass
plt.text(12, 17, "3 august 2019", fontsize=12)
plt.ylabel("UV Index")
plt.xlabel("Local time (h)")
plt.xlim(5, 20)
plt.ylim(0, 16)
plt.yticks(np.arange(0, 17))
plt.xticks(np.arange(5, 21))
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.legend(frameon=False,
           ncol=8,
           fontsize=8,
           bbox_to_anchor=(1.04, 1.01, 0.05, 0.05)
           )
plt.show()
