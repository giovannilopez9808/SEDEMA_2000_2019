from Class_list import *


def select_data(data=pd.DataFrame(), parameters={}):
    data = data[data.index.hour >= parameters["Hour initial"]]
    data = data[data.index.hour <= parameters["Hour final"]]
    data = data[data.index.year >= parameters["Year initial"]]
    data = data[data.index.year <= parameters["Year final"]]
    data = data[data.index.month >= parameters["Month initial"]]
    data = data[data.index.month <= parameters["Month final"]]
    data = obtain_daily_maximum(data)
    return data


parameters = {
    "path data": "../Data/SEDEMA_Data/Radiation/",
    "path results": "../Data/",
    "wavelength": "UVB",
    "Hour initial": 11,
    "Hour final": 15,
    "Month initial": 6,
    "Month final": 7,
    "Year initial": 2000,
    "Year final": 2001,
}
SEDEMA_data = SEDEMA_data_set(path=parameters["path data"],
                              type_name=parameters["wavelength"])
data = select_data(data=SEDEMA_data.data,
                   parameters=parameters)
mean = data.mean()["value"]
std = data.std()["value"]
print("Mean\tStd")
print("{:.1f}\t{:.4f}".format(mean,
                              std))
