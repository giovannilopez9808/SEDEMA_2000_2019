import pandas as pd
import os


def date_format(data):
    data["Dates"] = data[date_name].str[6:10]+"-" + \
        data[date_name].str[3:5]+"-"+data[date_name].str[0:2]
    data["Hour"] = data[date_name].str[11:13]
    data["Hour"] = data["Hour"].astype(int)-1
    data["Hour"] = data["Hour"].astype(str).str.zfill(2)
    data["Dates"] = data["Dates"]+" "+data["Hour"]
    data.index = pd.to_datetime(data["Dates"])
    data = data.drop([date_name, "Dates", "Hour"], 1)
    return data


inputs = {
    "path data": "../Data/SEDEMA_Data/",
    "folders": ["Radiation"],
    "data type": {
        "Pollutants": {
            "skiprows": 10,
            "Date column": "date"
        },
        "Radiation": {
            "skiprows": 8,
            "Date column": "Date"
        }
    }
}
for folder in inputs["folders"]:
    path = inputs["path data"]+folder+"/"
    skiprows = inputs["data type"][folder]["skiprows"]
    date_name = inputs["data type"][folder]["Date column"]
    files = sorted(os.listdir(path))
    for file in files:
        print("Formateando {}".format(file))
        data = pd.read_csv(path+file, skiprows=skiprows)
        data = date_format(data)
        data.to_csv(path+file)
