import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def select_files(files=[], type_name=""):
    """
    Selecciona el nombre de los Data
    dependiendo la información que contienen.
    -----------------------------------------------------
    #### Input:
    type_name : String con el posible valor de UVA o UVB
    files     : Lista con los nombres de los Data por
                filrar
    -----------------------------------------------------
    #### Return 
    files_type: Lista con los nombres de los Data que
                contienen type_name en sus nombres
    ------------------------------------------------------
    """
    files_type = []
    for file in files:
        if type_name in file:
            files_type.append(file)
    return files_type


def read_data(path="", name=""):
    """
    Lectura estandarizada de los datos
    -----------------------------------------------------
    #### Inputs:
    path    : Localizacion de los datos
    name    : nombre del archivo con los datos
    -----------------------------------------------------
    #### Return:
    data    : datos contenidos en name con el indice
              estandarizado en fechas
    -----------------------------------------------------
    """
    data = pd.read_csv("{}{}".format(path,
                                     name),
                       index_col=0)
    data = format_date_data(data)
    return data


def format_date_data(data=pd.DataFrame([])):
    """
    Formateo y eliminación de columnas innecesarias de los
    datos
    -----------------------------------------------------
    #### Inputs:
    data    : DataFrame con los datos a formatear
    -----------------------------------------------------
    #### Return:
    data    : Dataframe con las columnas parameter y unit 
              eliminadas y como indice de las fechas
              estandarizadas
    """
    data.index = pd.to_datetime(data.index)
    data = data.drop(["parameter",
                      "unit", ],
                     1)
    return data


def clean_data(data=pd.DataFrame([]), hour_i=0, hour_f=24):
    """
    Limpíeza de loss datos a seleccionando una hora inicial
    y hora final
    -----------------------------------------------------
    #### Inputs:
    data    : Dataframe que contiene los datos sin filtrar por horas
    hour_i  : Hora inicial donde se realizara el filtro de datos
    hour_f  : Hora final donde se realizara el filtro de datos
    -----------------------------------------------------
    #### Return:
    data    : Dataframe con los datos filtrados
    """
    data = data[data.index.hour >= hour_i]
    data = data[data.index.hour <= hour_f]
    return data


def obtain_daily_maximum_per_stations(data=pd.DataFrame([])):
    """
    Obtiene el maximo diario de cada estacion a partir de 
    un dataframe
    -----------------------------------------------------
    #### Inputs:
    data    : Dataframe con los datos de cada estacion en
              columna cve_station
    -----------------------------------------------------
    #### return:
    Dataframe con doble indice, fecha y estación, para cada fecha
    y estación existirá un máximo
    """
    return data.groupby("cve_station").resample("D").max()


def format_data(data=pd.DataFrame(), resize=1):
    """
    Escalamiento de los datos de irradiancia solar eritemica
    a indice UV
    -----------------------------------------------------
    #### Inputs:
    data    : Dataframe con los datos en la columna value
    resize  : Escalamiento de los datos de la SEDEMA
              (unit to eritemica)
    -----------------------------------------------------
    #### Return: 
    data    : Dataframe con los datos en IUV en la columna value
    """
    data["value"] = data["value"]*40*resize
    data = data.dropna()
    return data


def plot_grid(UV_max=15, percentage_limit=50):
    """
    Ploteo de las grillas, impares más claras que las pares
    -----------------------------------------------------
    Inputs:
    UV_max              : Maximo valor de UV que se graficara
    percentage_limit    : Valor maximo del porcentaje
    -----------------------------------------------------
    """
    even = np.arange(0, percentage_limit+2, 2)
    odd = even-1
    for i in range(np.size(even)):
        plt.plot([-4,  UV_max+1],
                 [even[i], even[i]],
                 color="black",
                 ls="--",
                 alpha=0.5)
        plt.plot([-4, UV_max+1],
                 [odd[i], odd[i]],
                 color="gray",
                 ls="--",
                 alpha=0.3)


def obtain_xticks(UV_values=[]):
    """
    Obtiene los valores que se imprimiran en las xticks
    -----------------------------------------------------
    Inputs:
    UV_values   : Lista de valores de UV
    -----------------------------------------------------
    Returns:
    Valores de UV_values añadiendo el ultimo valor más 1
    """
    return np.append(UV_values, UV_values[-1]+1)


def obtain_yticks(percentage_limit=50):
    """
    Obtiene los valores que se imprimiran en las yticks
    -----------------------------------------------------
    Inputs:
    percentage_limit    : Valor maximo que se graficara
    -----------------------------------------------------
    Returns:
    Lista de valores de dos en dos hasta llegar el valor
    percentage_limit
    """
    return np.arange(0, percentage_limit+2, 2)


def autolabel(rects):
    """
    Attach a text UV_values above each bar in *rects*, displaying its height.
    """
    for i, rect in enumerate(rects):
        height = rect.get_height()
        ax.annotate("{:.2f}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center',
                    va='bottom',
                    fontsize=10)


parameters = {
    "path data": "../Data/SEDEMA_Data/Radiation/",
    "path graphics": "../Graphics/",
    "graphics name": "Histogram",
    "font size": 15,
    "wavelength": {  # "UVA": 10,
        "UVB": 0.0583, },
    "hour initial": 11,
    "hour final": 15,
    "UV minium": 1,
    "UV maximum": 16,
    "Percentage limit": 20,
}
UV_count = np.zeros(parameters["UV maximum"]-parameters["UV minium"])
UV_values = np.arange(parameters["UV minium"],
                      parameters["UV maximum"])
files = sorted(os.listdir(parameters["path data"]))
n_total = 0
for wavelength in parameters["wavelength"]:
    resize = parameters["wavelength"][wavelength]
    files_type = select_files(files,
                              wavelength)
    for file in files_type:
        if not "2020" in file:
            print("Analizando archivo {}".format(file))
            data = read_data(parameters["path data"],
                             file)
            data = clean_data(data,
                              parameters["hour initial"],
                              parameters["hour final"])
            data = obtain_daily_maximum_per_stations(data)
            data = format_data(data,
                               resize)
            for index in data.index:
                UV = data["value"][index]
                if parameters["UV maximum"] >= UV >= parameters["UV minium"]:
                    UV = int(UV-parameters["UV minium"])
                    UV_count[UV] += 1
                    n_total += 1
UV_count = UV_count*100/n_total
fig, ax = plt.subplots(figsize=(9, 7))
plt.ylim(0, 20)
plt.xlim(-1, parameters["UV maximum"]+1)
plt.xlabel("Daily maximums UV Index",
           fontsize=parameters["font size"])
plt.ylabel("Frequency (%) of Days",
           fontsize=parameters["font size"])
plt.title("Period 2000-2019",
          fontsize=parameters["font size"])
rects = ax.bar(UV_values, UV_count,
               color="#00838a",
               width=1,
               edgecolor="black")
autolabel(rects)
plot_grid(parameters["UV maximum"],
          parameters["Percentage limit"])
xticks = obtain_xticks(UV_values)
yticks = obtain_yticks(parameters["Percentage limit"])
plt.xticks(xticks-0.5,
           xticks,
           fontsize=parameters["font size"])
plt.yticks(yticks,
           fontsize=parameters["font size"])
# <--------Guardado de la grafica-------------->
plt.subplots_adjust(left=0.102,
                    bottom=0.093,
                    right=0.962,
                    top=0.936)
plt.savefig("{}{}.png".format(parameters["path graphics"],
                              parameters["graphics name"]),
            dpi=400)
# plt.show()
