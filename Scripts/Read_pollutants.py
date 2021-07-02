from functions import *
from os import listdir
import numpy as np
import datetime


inputs = {
    "hour initial": 11,
    "hour final": 15,
    "pollutants": ["CO",
                   "O3",
                   "NO2",
                   "PM10",
                   "SO2"],
    "path data": "../Data/SEDEMA_Data/Pollutants/",
    "path stations": "../Stations/",
    "file": "CDMX.csv"
}
stations = sorted(listdir(inputs["path stations"]))
files = sorted((listdir(inputs["path data"])))
n_param = len(inputs["pollutants"])
info = np.zeros([n_param, 365, 20, 2])
for file in files:
    dates, stations_name, parameters_name, data_list = np.loadtxt(inputs["path data"]+file,
                                                                  skiprows=11, usecols=[0, 1, 2, 3],
                                                                  delimiter=",",
                                                                  dtype=str,
                                                                  unpack=True)
    print("Analizando "+file)
    for date, station_name, pollutant_name, data in zip(dates, stations_name, parameters_name, data_list):
        date, hour = obtain_date_and_hour(date)
        # <---------------------------------Verificacion de la hora--------------------------->
        if inputs["hour initial"] <= hour <= inputs["hour final"]:
            conseday = obtain_day_consecutive(date)
            # <-------------------------Verificacion de que el dato exista-------------->
            if data != "":
                # <-----------------------------Verificacion del parametro---------------------->
                if pollutant_name in inputs["pollutants"]:
                    loc_parameter = find_location(pollutant_name,
                                                  inputs["pollutants"])
                    # <---------------------Verificacion de la estacion--------------------->
                    if station_name in stations:
                        year = date.year-2000
                        info[loc_parameter, conseday,
                             year, 0] += float(data)
                        info[loc_parameter, conseday, year, 1] += 1
# <---------------------------------Escritura de los Data---------------------------------->
print("Calculando promedios y escribiendo Data")
for parameter, n in zip(inputs["pollutants"], range(n_param)):
    file = open("../Data/"+parameter+"_"+inputs["file"], "w")
    file.write("Date")
    for year in range(20):
        file.write(",{}".format(year+2000))
    file.write("\n")
    for day in range(365):
        date = conseday_to_date(day, 2001)
        date = date_formtat_mmdd(date)
        file.write(date)
        for year in range(20):
            if info[n, day, year, 1] != 0:
                info[n, day, year, 0] = np.round(
                    info[n, day, year, 0]/info[n, day, year, 1], 3)
            else:
                info[n, day, year, 0] = -99
            file.write(",{}".format(info[n, day, year, 0]))
        file.write("\n")
    file.close()
