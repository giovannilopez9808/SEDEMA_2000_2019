import pandas as pd


def date_format(data):
    data["Date"] = data["Datetime"].str[0:4]+"-" + \
        data["Datetime"].str[4:6]+"-"+data["Datetime"].str[6:8]
    data["Date"] = pd.to_datetime(data["Date"])
    data.index = data["Date"]
    data = data.drop(["Date", "Datetime"], 1)


inputs = {
    "path data": "../Data/",
    "file data": "Data_OMI_",
    "product": "OMTO3",
    "skiprows": 27,
    "column": "Cld. F.",
    "file results": "Cloud_factor"
}
data = pd.read_fwf(inputs["path data"]+inputs["file data"]+inputs["product"]+".dat",
                   skiprows=inputs["skiprows"])
date_format(data)
data_UVI = data[inputs["column"]]
data_UVI = data_UVI[data_UVI.index >= "2005-01-01"]
data_UVI = data_UVI[data_UVI.index <= "2019-12-31"]
data_UVI.to_csv(inputs["path data"] +
                inputs["file results"]+".csv",
                float_format='%.4f')
