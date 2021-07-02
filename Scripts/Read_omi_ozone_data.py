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


def create_data_in_matrix(data, column):
    dates = data.index.drop_duplicates()
    years = obtain_headers(dates)
    dates = obtain_index(dates)
    data_matrix = create_data_matrix(dates,
                                     years)
    for date in data.index:
        header = date.date().year
        index = str(date.date())[5:10]
        data_matrix[header][index] = data[column][str(date.date())].mean()
    return data_matrix


def obtain_headers(dates):
    years = dates.year.drop_duplicates()
    return years


def obtain_index(dates):
    dates = dates.astype(str).str[5:10]
    dates = dates.drop_duplicates()
    dates = dates.drop("02-29")
    dates = sorted(dates)
    return dates


def create_data_matrix(index, header):
    data_matrix = pd.DataFrame(index=index,
                               columns=header)
    return data_matrix


inputs = {
    "path data": "../Data/",
    "file data": "Data_OMI_",
    "product": "OMTO3",
    "skiprows": 27,
    "columns": "Ozone",
    "file results": "O3_OMI",
    "day initial": "2005-01-01",
    "day final": "2019-12-31",
}
data = pd.read_fwf(inputs["path data"]+inputs["file data"]+inputs["product"]+".dat",
                   skiprows=inputs["skiprows"])
data = date_format(data)
data = clean_data(data,
                  inputs["columns"])
data = obtain_data_in_period(data,
                             inputs["day initial"],
                             inputs["day final"])
data_matrix = create_data_in_matrix(data,
                                    inputs["columns"])
data_matrix.to_csv("{}{}.csv".format(inputs["path data"],
                                     inputs["file results"]),
                   float_format='%.4f')
