import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime


def obtain_mean_and_std(data):
    data = data.astype(float)
    mean = data.resample("MS").mean()
    std = data.resample("MS").std()
    return mean, std


def format_data(data):
    index = obtain_index(data)
    data_flat = pd.DataFrame(index=index,
                             columns=["Data"],)
    data_flat.index = pd.to_datetime(data_flat.index)
    for year in data.columns:
        for date in data.index:
            index = year+"-"+date
            value = data[year][date]
            data_flat["Data"][index] = float(value)
    return data_flat


def obtain_index(data):
    years = data.columns
    year_i = int(years[0])
    year_f = int(years[-1])
    days = (datetime.date(year_f, 12, 31)-datetime.date(year_i, 1, 1)).days
    index = []
    for day in range(days+1):
        date = datetime.date(year_i, 1, 1)+datetime.timedelta(days=day)
        index.append(str(date))
    return index


def format_xticks(data):
    index = data.index
    tick = []
    years = []
    dates = []
    year_i = int(str(index[0])[0:4])
    year_f = int(str(index[-1])[0:4])
    for value in index:
        value = str(value)[0:10]
        tick.append(value)
    for year in range(year_i, year_f+1):
        date = datetime.date(year, 1, 1)
        dates.append(str(date))
        years.append(year)
    return tick, years, dates


inputs = {
    "CO": {
        "tick": "CO",
        "color": "purple",
        "title": "CO (ppm)",
        "lim sup": 5,
        "lim inf": 0,
        "delta": 1
    },
    "PM10": {
        "tick": "PM$_{10}$",
        "color": "#A25715",
        "title": "PM$_{10}$ ($\mu g/m^3$)",
        "lim sup": 95,
        "lim inf": 15,
        "delta": 20
    },
    "NO2": {
        "tick": "NO$_2$",
        "color": "blue",
        "title": "NO$_2$, SO$_2$ (ppb)",
        "lim sup": 70,
        "lim inf": 0,
        "delta": 10
    },
    "O3": {
        "tick": "O$_3$",
        "color": "green",
        "title": "O$_3$ (ppb)",
        "lim sup": 120,
        "lim inf": 20,
        "delta": 20
    },
    "AOD": {
        "tick": "AOD$_{340}$",
        "color": "#CB258C",
        "title": "AERONET AOD$_{340}$",
        "lim sup": 1.4,
        "lim inf": 0,
        "delta": 0.2
    },
    "SO2": {
        "tick": "SO$_{2}$",
        "color": "black",
        "title": "NO$_2$, SO$_2$ (ppb)",
        "lim sup": 70,
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
for input, ax in zip(inputs, axs):
    print("Analizando {}".format(input))
    # Parametros para la grafica dependiendo del compuesto
    tick = inputs[input]["tick"]
    color = inputs[input]["color"]
    title = inputs[input]["title"]
    lim_inf = inputs[input]["lim inf"]
    lim_sup = inputs[input]["lim sup"]
    delta = inputs[input]["delta"]
    # Direccion del archivo de datos
    file = parameters["path data"]+input+"_"+parameters["file data"]
    # Lectura de datos
    data = pd.read_csv(file,
                       index_col=0)
    data_flat = format_data(data)
    mean, std = obtain_mean_and_std(data_flat)
    x, years, dates = format_xticks(mean)
    ax.plot(x, mean["Data"],
            ls="-",
            label=tick,
            color=color,
            linewidth=parameters["linewidth"])
    # ax.errorbar(x, mean["Data"],
    #             yerr=std["Data"],
    #             marker="o",
    #             linewidth=parameters["linewidth"],
    #             # ls="--",
    #             alpha=0.6,
    #             color=color,
    #             capsize=5,
    #             markersize=2,
    #             label=tick,
    #             )
    ax.set_xlim(x[0],
                x[-1])
    ax.set_xticks([])
    ax.set_ylim(lim_inf, lim_sup)
    yticks = np.arange(lim_inf, lim_sup+delta, delta)
    ax.set_yticks(yticks)
    ax.set_xticks(dates)
    ax.set_xticklabels(years,
                       rotation=60)
    if ax in [ax2, ax5]:
        ax.set_ylabel(title,
                      rotation=-90,
                      va="bottom")
    else:
        ax.set_ylabel(title)
    if ax in [ax1, ax4]:
        ax.legend(frameon=False,
                  # ncol=2,  # loc="best",
                  loc="upper right",
                  bbox_to_anchor=(0.8, 1))
    else:
        ax.legend(frameon=False,
                  ncol=2,
                  loc="upper right")
#plt.savefig(parameters["path graphics"]+"pollutants.png", dpi=400)
plt.show()
