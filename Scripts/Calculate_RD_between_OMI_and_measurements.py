import matplotlib.pyplot as plt
import pandas as pd
import os


def read_OMI_data(path="", name=""):
    """
    Lectura de los datos de OMI
    #### inputs
    path -> direccion donde se encuentran los datos

    name -> nombre del archivo
    """
    # Lectura cruda de los datos
    data = pd.read_csv("{}UVI_{}.csv".format(path,
                                             name),
                       index_col=0)
    # Formato de fecha a los datos
    data = format_data(data)
    return data


def format_data(data=pd.DataFrame()):
    """
    Formato de fecha en el indice del dataframe
    """
    data.index = pd.to_datetime(data.index)
    return data


def obtain_monthly_mean(data=pd.DataFrame()):
    """
    Calculo del promedio mensual a partir de un dataframe
    """
    return data.resample("MS").mean()


def read_SEDEMA_data(path="", resize=1):
    """
    Lectura de los datos de la SEDEMA
    #### inputs
    path -> direccion donde se encuentran los datos

    resize -> valor para convertir los datos a UVI
    """
    # Listado de los archivos de la SEDEMA
    files = sorted(os.listdir(path))
    # Seleccionar unicamente los de UVB
    files = select_SEDEMA_files(files=files,
                                type_name="UVB")
    # Ciclo para reunir todos los archivos en un solo dataframe
    for i, file in enumerate(files):
        if i == 0:
            # Lectura de los datos de la SEDEMA
            data = read_SEDEMA_data_each_file(path,
                                              file)
        else:
            # Lectura de los datos de la SEDEMA
            data_year = read_SEDEMA_data_each_file(path,
                                                   file)
            # Union de todos los dataframe en uno solo
            data = data.append(data_year)
    # Obtener el máximo diario de todas las estaciones
    data = obtain_daily_maximum(data)
    # Redimensionar los datos UVI
    data["value"] = data["value"]*resize
    return data


def select_SEDEMA_files(files=[], type_name=""):
    """
    Descarta los archivos dependiendo si contienen un nombre en especifico
    #### inputs
    files -> listado de los archivos sin filtrar

    type_name -> nombre con el cual se filtraran los archivos
    """
    files_type = []
    for file in files:
        # Filtrado
        if type_name in file:
            files_type.append(file)
    return files_type


def read_SEDEMA_data_each_file(path="", name=""):
    """
    Lectura de cada archivo de datos de la SEDEMA
    """
    # Lectura cruda de los datos
    data = pd.read_csv("{}{}".format(path,
                                     name),
                       index_col=0)
    # Formateo del dataframe
    data = format_SEDEMA_data(data)
    return data


def format_SEDEMA_data(data=pd.DataFrame()):
    """
    Elimina columnas innecesarias y realiza el formato de fecha al indice del dataframe
    """
    # Formato de fecha al indice
    data.index = pd.to_datetime(data.index)
    # Eliminacion de columnas inncesarias
    data = data.drop(["parameter",
                      "unit",
                      "cve_station"],
                     1)
    return data


def obtain_daily_maximum(data=pd.DataFrame()):
    """
    Calculo del promedio maximo diario
    """
    return data.resample("D").max()


def select_data(data=pd.DataFrame(), date_initial="2005-01-01", date_final="2019-12-31"):
    """
    Selecciona los datos que se encuentran dentro de un periodo
    """
    data = data[data.index >= date_initial]
    data = data[data.index <= date_final]
    return data


def obtain_xticks(date_initial="2005-01-01", date_final="2019-12-31"):
    """
    obtiene los ticks labels dependiendo del periodo en donde se hara el analisis
    """
    year_initial = int(date_initial[0:4])
    year_final = int(date_final[0:4])
    years = [year for year in range(year_initial, year_final+2)]
    dates = [pd.to_datetime("{}-01-01".format(year)) for year in years]
    return dates, years


parameters = {
    "path data": "../Data/",
    "path graphics": "../Graphics/",
    "OMI column": "CSUVindex",
    "path SEDEMA data": "../Data/SEDEMA_Data/Radiation/",
    "wavelength": {"UVA": 10,
                   "UVB": 0.0583*40, },
    "Year initial": "2005-01-01",
    "Year final": "2019-12-31",
}
# Lectura de los datos de OMI
OMI_data = read_OMI_data(parameters["path data"],
                         parameters["OMI column"])
# Calculo del promedio mensual
OMI_monthly_mean = obtain_monthly_mean(OMI_data)
# Seleccionar datos que estan dentro del periodo
OMI_monthly_mean = select_data(data=OMI_monthly_mean,
                               date_initial=parameters["Year initial"],
                               date_final=parameters["Year final"])
monthly_mean = pd.DataFrame(index=OMI_monthly_mean.index)
monthly_mean["OMI"] = OMI_monthly_mean["CSUVindex"]
# Lectura de los datoa de SEDEMA
SEDEMA_data = read_SEDEMA_data(path=parameters["path SEDEMA data"],
                               resize=parameters["wavelength"]["UVB"])
# Calculo del promedio mensual
SEDEMA_monthly_mean = obtain_monthly_mean(SEDEMA_data)
# Seleccionar datos que estan dentro del periodo
SEDEMA_monthly_mean = select_data(data=SEDEMA_monthly_mean,
                                  date_initial=parameters["Year initial"],
                                  date_final=parameters["Year final"])
monthly_mean["SEDEMA"] = SEDEMA_monthly_mean["value"]
# Calculo de la RD
monthly_mean["RD"] = (monthly_mean["OMI"] -
                      monthly_mean["SEDEMA"])/monthly_mean["SEDEMA"]*100
monthly_mean.to_csv("{}Monthly_mean_RD.csv".format(parameters["path data"]),
                    float_format="%.2f")
print("La diferencial relativa promedio es {:.2f}".format(
    monthly_mean["RD"].mean()))
# Inicio del ploteo de los datos
dates, years = obtain_xticks(parameters["Year initial"],
                             parameters["Year final"])
plt.figure(figsize=(10, 4))
plt.subplots_adjust(left=0.055,
                    bottom=0.09,
                    right=0.971,
                    top=0.926)
plt.xlim(pd.to_datetime(parameters["Year initial"]),
         pd.to_datetime(parameters["Year final"]))
plt.xticks(dates, years)
plt.ylim(0, 120)
plt.yticks([tick for tick in range(0, 120, 10)])
plt.scatter(monthly_mean.index, monthly_mean["RD"])
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.show()
