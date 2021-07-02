import pandas as pd
import os


def select_files(files, type_name):
    files_type = []
    for file in files:
        if type_name in file:
            files_type.append(file)
    return files_type


def read_data(path, name):
    data = pd.read_csv("{}{}".format(path,
                                     name),
                       index_col=0)
    data = format_date_data(data)
    return data


def format_date_data(data):
    data.index = pd.to_datetime(data.index)
    data = data.drop(["parameter",
                      "unit",
                      "cve_station"],
                     1)
    return data


def format_results(data, resize):
    data = data*resize
    data = data.round({
        "value": 2,
        "std": 4,
    })
    return data


inputs = {
    "path data": "../Data/SEDEMA_Data/Radiation/",
    "path results": "../Data/",
    "wavelength": {"UVA": 10,
                   "UVB": 0.0583*40, },
    "Hour initial": 11,
    "Hour final": 15,
    "Month initial": 6,
    "Month final": 7,
    "Year initial": 2000,
    "Year final": 2001,
}
files = sorted(os.listdir(inputs["path data"]))
for wavelength in inputs["wavelength"]:
    resize = inputs["wavelength"][wavelength]
    files_type = select_files(files,
                              wavelength)
    for i, file in enumerate(files_type):
        print("Analizando archivo {}".format(file))
        if i == 0:
            data_all = read_data(inputs["path data"],
                                 file)
        else:
            data = read_data(inputs["path data"],
                             file)
            data_all = data_all.append(data)
    data_all = data_all[data_all.index.hour >= inputs["Hour initial"]]
    data_all = data_all[data_all.index.hour <= inputs["Hour final"]]
    data_all = data_all[data_all.index.year >= inputs["Year initial"]]
    data_all = data_all[data_all.index.year <= inputs["Year final"]]
    data_all = data_all[data_all.index.month >= inputs["Month initial"]]
    data_all = data_all[data_all.index.month <= inputs["Month final"]]
    data_all = data_all.resample("D").max()
    print(data_all.max()*resize)
