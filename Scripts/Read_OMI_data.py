import matplotlib.pyplot as plt
import pandas as pd


def date_format(data):
    data["Date"] = data["Datetime"].str[0:4]+"-" + \
        data["Datetime"].str[4:6]+"-"+data["Datetime"].str[6:8]
    data["Date"] = pd.to_datetime(data["Date"])
    data.index = data["Date"]
    data = data.drop(["Date", "Datetime"], 1)
    return data


def clean_data(data, columns):
    for column in data.columns:
        if not column in columns:
            data = data.drop(column, 1)
    return data


def obtain_data_in_period(data, date_i, date_f):
    data = data[data.index >= date_i]
    data = data[data.index <= date_f]
    return data


def drop_data_useless(data, columns, limit):
    for column in columns:
        data = data[data[column] < limit]
    return data


inputs = {
    "path data": "../Data/",
    "file data": "Data_OMI_",
    "product": "OMUVB",
    "skiprows": 50,
    "UVI limit": 18,
    "UVIcolumns": ["CSUVindex", "UVindex"],
    "file results": "UVI_",
    "day initial": "2005-01-01",
    "day final": "2019-12-31",
}
data = pd.read_fwf(inputs["path data"]+inputs["file data"]+inputs["product"]+".dat",
                   skiprows=inputs["skiprows"])
data = date_format(data)
data = clean_data(data,
                  inputs["UVIcolumns"])
data = obtain_data_in_period(data,
                             inputs["day initial"],
                             inputs["day final"])
data = drop_data_useless(data,
                         inputs["UVIcolumns"],
                         inputs["UVI limit"])
print(data.max())
for uvicolumn in inputs["UVIcolumns"]:
    print("Creando archivo {}".format(uvicolumn))
    data_UVI = data[uvicolumn]
    print(data_UVI.count())
    data_UVI.to_csv("{}{}{}.csv".format(inputs["path data"],
                                        inputs["file results"],
                                        uvicolumn),
                    float_format='%.4f')
