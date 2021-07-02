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


def obtain_moving_average_monthly(data=pd.DataFrame(), month=3):
    """
    Obtiene el moving average a partir de un dataframe
    --------------------------------------------
    Inputs:
    data    : Dataframe que contiene los datos
    month   : Numero en el cual se realizara el moving
              average
    --------------------------------------------
    Return:
    Dataframe con el moving average
    """
    return data.rolling(window=month).mean()


def cut_data(data=pd.DataFrame(), date_i="2000-12-31", date_f="2020-12-31"):
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
    "graphics name": "UV_Moving_Average2",
    "path data": "../Data/",
    "file data": "Max_Monthly_UVB.csv",
    "file moving average": "Moving_average_UVI",
    "file Max Monthly UVI": "Max_Monthly_UVI",
    "file Fit UVI": "Fit_UVI",
    "Months moving Average": 3,
    "year initial": 2000,
    "year final": 2019,

}
data = read_data(parameters["path data"],
                 parameters["file data"])
# <------------Moving average------------->
moving_average_data = obtain_moving_average_monthly(data["Max"],
                                                    parameters["Months moving Average"])
data = cut_data(data,
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
years.append(2020)
years = np.array(years)
Fit_line = fit(years)
# <-------Inicio de la grafica UVyearlyError-------->
plt.xticks((years-parameters["year initial"])*12,
           years,
           rotation=60,
           fontsize=12)
plt.yticks(fontsize=12)
plt.title("Period 2000-2019",
          fontsize="large")
plt.ylabel("UV Index",
           fontsize="large")
plt.xlim(0,
         (parameters["year final"]-parameters["year initial"]+1)*12)
plt.ylim(0,
         16)
# Barras de error
plt.errorbar(range(len(data["Max"])),
             list(data["Max"]),
             yerr=data["std"],
             marker="o",
             linewidth=1,
             ls="None",
             alpha=0.8,
             color="black",
             capsize=5,
             markersize=2,
             label="Monthly average and SD")
# Ploteo del moving average para 3 meses
plt.plot(range(len(moving_average_data)),
         list(moving_average_data),
         label="Moving average",
         linewidth=3,
         color="#118ab2",
         alpha=0.75)
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
plt.legend(ncol=3,
           mode="expand",
           frameon=False,
           fontsize="small")
# Guardado de la grafica
plt.savefig("{}{}.png".format(parameters["path graphics"],
                              parameters["graphics name"]),
            dpi=400)
# Write Max Monthly UVI
data.to_csv("{}{}.csv".format(parameters["path data"],
                              parameters["file Max Monthly UVI"]),
            float_format="%.2f")
# Write Moving average results
moving_average_data.to_csv("{}{}.csv".format(parameters["path data"],
                                             parameters["file moving average"]),
                           float_format="%.1f")
# Write Fit Results
file_fit = open("{}{}.csv".format(parameters["path data"],
                                  parameters["file Fit UVI"]),
                "w")
file_fit.write("Years,Fit\n")
for year, fit in zip(years, Fit_line):
    file_fit.write("{},{:.4f}\n".format(year,
                                        fit))
file_fit.close()
