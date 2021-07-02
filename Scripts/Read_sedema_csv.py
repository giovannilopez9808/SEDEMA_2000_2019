from functions import *
import pandas as pd
import os

inputs = {
    "path data": "../Data/SEDEMA_Data/Radiation/",
    "path stations": "../Stations/",
    "Wave": {
        "UVA": {
            "folder": "UVA",
            "name": "UVA",
            "change units": 10,
        },
        "UVB": {
            "folder": "Erythemal",
            "name": "Ery",
            "change units": 0.0583,
        }
    }
}
files = sorted(os.listdir(inputs["path data"]))
# <--------------Ciclo para analizar todos los Data----------->
for file in files:
    print("Analizando archivo {}".format(file))
    lon, year = file.split("_")
    year = year[0:4]
    folder = inputs["Wave"][lon]["folder"]
    name = inputs["Wave"][lon]["name"]
    resize = inputs["Wave"][lon]["change units"]
    data = pd.read_csv("{}{}".format(inputs["path data"],
                                     file)).fillna(0.0)
    data["Dates"] = pd.to_datetime(data["Dates"])
    data_len = data["Dates"].count()
    # Ciclo para leer las columnas
    for i in range(data_len):
        # Lectura del nombre de la estacion
        station = data["cve_station"][i]
        value = data["value"][i]
        hour = data["Dates"][i].hour
        date = date2yymmdd(data["Dates"][i].date())
        mkdir(station, path=inputs["path stations"])
        mkdir(folder, path="{}{}/".format(inputs["path stations"],
                                          station))
        path_station = inputs["path stations"]+station+"/"+folder+"/"
        file = open("{}{}.txt".format(path_station,
                                      date),
                    "a")
        file.write("{} {:.5f}\n".format(hour, float(value)*resize))
        file.close()
