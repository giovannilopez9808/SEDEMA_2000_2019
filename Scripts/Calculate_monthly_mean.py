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


def clean_data(data, hour_i, hour_f):
    data = data[data.index.hour >= hour_i]
    data = data[data.index.hour <= hour_f]
    return data


def obtain_daily_max(data):
    return data.resample("D").max()


def obtain_monthly_mean(data):
    return data.resample("MS").mean()


def obtain_monthly_std(data):
    return data.resample("MS").std()


def format_results(data, resize):
    data = data*resize
    data = data.round({
        "value": 4,
        "std": 4,
    })
    return data


inputs = {
    "path data": "../Data/SEDEMA_Data/Radiation/",
    "path results": "../Data/",
    "wavelength": {"UVA": 10,
                   "UVB": 0.0583, },
    "hour initial": 11,
    "hour final": 15,
}
files = sorted(os.listdir(inputs["path data"]))
for wavelength in inputs["wavelength"]:
    filename = "Max_Monthly_{}.csv".format(wavelength)
    results = open("{}{}".format(inputs["path results"],
                                 filename),
                   "w")
    results.write("Dates,Max,std\n")
    resize = inputs["wavelength"][wavelength]
    files_type = select_files(files,
                              wavelength)
    for file in files_type:
        print("Analizando archivo {}".format(file))
        data = read_data(inputs["path data"],
                         file)
        data = clean_data(data,
                          inputs["hour initial"],
                          inputs["hour final"])
        daily_max = obtain_daily_max(data)
        monthly_results = obtain_monthly_mean(daily_max)
        monthly_results["std"] = obtain_monthly_std(daily_max)
        monthly_results = format_results(monthly_results,
                                         resize)
        for date in monthly_results.index:
            results.write("{},{},{}\n".format(date,
                                              monthly_results["value"][date],
                                              monthly_results["std"][date]))
    results.close()
