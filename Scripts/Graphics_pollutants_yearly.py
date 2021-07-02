import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def obtain_mean_and_std(data):
    mean = data.mean()
    mean_clean = mean.dropna()
    std = data.std()
    x = mean_clean.index.astype(int)-2000
    return x, mean_clean, mean, std


parameters = {
    "CO": {
        "tick": "CO",
        "color": "purple",
        "title": "CO (ppm)",
        "lim sup": 4,
        "lim inf": 0,
        "delta": 1
    },
    "PM10": {
        "tick": "PM$_{10}$",
        "color": "#A25715",
        "title": "PM$_{10}$ ($\mu g/m^3$)",
        "lim sup": 75,
        "lim inf": 0,
        "delta": 15
    },
    "NO2": {
        "tick": "NO$_2$",
        "color": "blue",
        "title": "NO$_2$, SO$_2$ (ppb)",
        "lim sup": 50,
        "lim inf": 0,
        "delta": 10
    },
    "O3": {
        "tick": "O$_3$",
        "color": "green",
        "title": "O$_3$ (ppb)",
        "lim sup": 90,
        "lim inf": 50,
        "delta": 10
    },
    "AOD": {
        "tick": "AOD$_{340}$",
        "color": "#CB258C",
        "title": "AERONET AOD$_{340}$",
        "lim sup": 0.8,
        "lim inf": 0,
        "delta": 0.15
    },
    "SO2": {
        "tick": "SO$_{2}$",
        "color": "black",
        "title": "NO$_2$, SO$_2$ (ppb)",
        "lim sup": 50,
        "lim inf": 0,
        "delta": 10
    },
}
parameters = {
    "path data": "../Data/",
    "file data": "CDMX.csv",
    "path graphics": "../Graphics/",
    "linewidth": 4,
    "fontsize": 12
}
plt.rc('font',
       size=parameters["fontsize"])
plt.rc('xtick',
       labelsize=parameters["fontsize"])
plt.rc('ytick',
       labelsize=parameters["fontsize"]-1)
fig, (ax1, ax3, ax4) = plt.subplots(3,
                                    figsize=(9, 9),
                                    sharex=True)
plt.subplots_adjust(top=0.964,
                    bottom=0.11,
                    left=0.085,
                    right=0.903,
                    hspace=0.195,
                    wspace=0.2
                    )
ax2 = ax1.twinx()
ax5 = ax4.twinx()
axs = np.array([ax2, ax1, ax3, ax4, ax5, ax3])
print("Pollutant\t  m\tMean\t  e\t b")
for parameter, ax in zip(parameters, axs):
    # Parametros para la grafica dependiendo del compuesto
    tick = parameters[parameter]["tick"]
    color = parameters[parameter]["color"]
    title = parameters[parameter]["title"]
    lim_inf = parameters[parameter]["lim inf"]
    lim_sup = parameters[parameter]["lim sup"]
    delta = parameters[parameter]["delta"]
    # Direccion del archivo de datos
    file = "{}{}_{}".format(parameters["path data"],
                            parameter,
                            parameters["file data"])
    # Lectura de datos
    data = pd.read_csv(file,
                       index_col=0)
    x, mean_clean, mean, std = obtain_mean_and_std(data)
    fit = np.polyfit(x, list(mean_clean), 1)
    prom = round(np.mean(mean), 3)
    # Impresión de los dattos
    print("{}\t\t {:.2f}\t {:.1f}\t {:.1f}\t{:.2f}".format(parameter,
                                                           fit[0],
                                                           prom,
                                                           fit[0]*100/prom,
                                                           fit[1]))
    ax.plot(list(mean_clean.index.astype(int)-2000), list(mean_clean),
            ls="-",
            label=tick,
            color=color,
            linewidth=parameters["linewidth"])
    ax.set_xlim(0, 19)
    ax.set_ylim(lim_inf, lim_sup)
    yticks = np.arange(lim_inf, lim_sup+delta, delta)
    ax.set_yticks(yticks)
    ax.set_xticks(x)
    ax.set_xticklabels(mean.index,
                       rotation=60)
    if ax in [ax2, ax5]:
        ax.set_ylabel(title,
                      rotation=-90,
                      va="bottom")
    else:
        ax.set_ylabel(title)
    if ax in [ax1, ax4]:
        ax.legend(frameon=False,
                  ncol=2, loc="best",
                  bbox_to_anchor=(0.84, 1))
    else:
        ax.legend(frameon=False,
                  ncol=2,
                  loc="upper right")
plt.savefig(parameters["path graphics"]+"pollutants.png", dpi=400)
plt.show()
