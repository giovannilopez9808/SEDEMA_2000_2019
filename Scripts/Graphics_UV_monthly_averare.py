import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def read_data(path="", file=""):
    """
    Lectura de los datos
    --------------------------------------------
    Inputs:
    path    : Direccion donde se localizan los datos
    file    : Nombre del archivo donde se localizan los datos
    --------------------------------------------
    Return
    data    : Dataframe con el indice estandarizado en fechas
              y las columnas de los datos en IUV
    """
    # Lectura de los datos
    data = pd.read_csv("{}{}".format(path,
                                     file),
                       index_col=0)
    # Erythemal a UVI
    data["Max"] = data["Max"]*40
    data["std"] = data["std"]*40
    data.index = pd.to_datetime(data.index)
    return data


def obtain_xticks(years=[]):
    years.append(2020)
    years = np.array(years)
    xticks = []
    years_ticks = []
    for year in years:
        years_ticks.append((year-years[0])*12)
        if year % 5 != 0:
            year = ""
        xticks.append(year)
    return years, xticks, years_ticks


def select_data_from_period(data=pd.DataFrame(), date_i="2000-12-31", date_f="2020-12-31"):
    """
    Limpíeza de loss datos a seleccionando una fecha inicial
    y fecha final
    -----------------------------------------------------
    Inputs:
    data    : Dataframe que contiene los datos sin filtrar por horas
    hour_i  : Fecha inicial donde se realizara el filtro de datos
    hour_f  : Fecha final donde se realizara el filtro de datos
    -----------------------------------------------------
    Return:
    data    : Dataframe con los datos filtrados
    """
    data = data[data.index >= date_i]
    data = data[data.index <= date_f]
    return data


def obtain_yearly_mean(data=pd.DataFrame()):
    """
    Promedio anual a partir de un dataframe
    -----------------------------------------------------
    Inputs: 
    data    : Dataframe que contiene los datos
    -----------------------------------------------------
    Return 
    Dataframe con el promedio anual
    """
    return data.resample("Y").mean()


parameters = {
    "path graphics": "../Graphics/",
    "graphics name": "UV_Moving_Average",
    "path data": "../Data/",
    "file data": "Max_Monthly_UVB.csv",
    "file moving average": "UVI_monthly_average",
    "file Max Monthly UVI": "Max_Monthly_UVI",
    "file Fit UVI": "Fit_UVI",
    "Months moving Average": 3,
    "year initial": 2000,
    "year final": 2019,

}
data = read_data(parameters["path data"],
                 parameters["file data"])
data = select_data_from_period(data,
                               "2000-01-01",
                               "2019-12-01",)
# <--------------Tendencia----------------->
yearly_mean = obtain_yearly_mean(data)
mean_data = yearly_mean.mean()
fit = np.polyfit(list(yearly_mean.index.year),
                 list(yearly_mean["Max"]), 1)

print("Parameter\tm\tMean\tTendency")
print("UVI:\t\t{:.2f}\t{:.1f}\t{:.1f}".format(fit[0],
                                              mean_data["Max"],
                                              fit[0]*100/mean_data["Max"]))

fit = np.poly1d(fit)
years = list(yearly_mean.index.year)
years, xticks, years_ticks = obtain_xticks(years)
Fit_line = fit(years)
# <-------Inicio de la grafica UVyearlyError-------->
plt.xticks(years_ticks,
           xticks,
           fontsize=12)
plt.yticks(fontsize=12)
plt.ylabel("UV Index",
           fontsize="large")
plt.xlabel("Year",
           fontsize="large")
plt.xlim(0,
         (parameters["year final"]-parameters["year initial"]+1)*12)
plt.ylim(2,
         16)
data["Max+sd"] = data["Max"]+data["std"]
data["Max-sd"] = data["Max"]-data["std"]
# Barras de error
plt.fill_between(range(len(data["Max"])),
                 list(data["Max+sd"]),
                 list(data["Max-sd"]),
                 color="#cadefb",
                 label="Monthly average $\pm$ SD")
plt.plot(range(len(data["Max"])),
         list(data["Max"]),
         color="#000000")
# Ploteo de linear fit
plt.plot((years-parameters["year initial"])*12,
         Fit_line,
         label="Linear fit",
         color="#d00000",
         linewidth=3)
plt.subplots_adjust(top=0.922,
                    bottom=0.147,
                    left=0.109,
                    right=0.948,
                    hspace=0.2,
                    wspace=0.2
                    )
plt.legend(ncol=2,
           frameon=False,
           loc="upper center")
plt.tight_layout()
# Guardado de la grafica
plt.savefig("{}{}.png".format(parameters["path graphics"],
                              parameters["graphics name"]),
            dpi=400)
# Write Max Monthly UVI
data.to_csv("{}{}.csv".format(parameters["path data"],
                              parameters["file Max Monthly UVI"]),
            float_format="%.2f")
# Write Moving average results
# moving_average_data.to_csv("{}{}.csv".format(parameters["path data"],
#                                              parameters["file moving average"]),
#                            float_format="%.1f")
# Write Fit Results
file_fit = open("{}{}.csv".format(parameters["path data"],
                                  parameters["file Fit UVI"]),
                "w")
file_fit.write("Years,Fit\n")
for year, fit in zip(years, Fit_line):
    file_fit.write("{},{:.4f}\n".format(year,
                                        fit))
file_fit.close()
