import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import datetime


class data_boxes:
    def __init__(self):
        self.init_data()

    def init_data(self):
        self.data_per_month = {}
        self.months = obtain_month_names()
        for month in self.months:
            self.data_per_month[month] = []

    def fill_data(self, data=pd.DataFrame()):
        for i, month in enumerate(self.months):
            data_month = data[data.index.month == i+1]
            self.data_per_month[month] = list(data_month["Max"])
        self.create_dataframe()

    def create_dataframe(self):
        self.data_per_month = pd.DataFrame(self.data_per_month)


class plot_boxes:
    def __init__(self, data=pd.DataFrame(), length=0.25, path="", filename=""):
        self.data = data
        self.length = length
        self.obtain_measures_of_central_tendency(path, filename)
        self.plot()

    def obtain_measures_of_central_tendency(self, path="", filename=""):
        self.central_data = self.data.describe()
        self.central_data = self.central_data.transpose()
        self.central_data["10%"] = self.data.quantile(q=0.1)
        self.central_data["90%"] = self.data.quantile(q=0.9)
        print(self.central_data)
        self.central_data["10%"] = self.central_data["mean"] - \
            self.central_data["10%"]
        self.central_data["90%"] = self.central_data["90%"] - \
            self.central_data["mean"]
        self.central_data.to_csv("{}{}".format(path,
                                               filename))

    def plot(self):
        plt.ylim(0, 14)
        plt.yticks([i for i in range(0, 15, 1)])
        plt.errorbar(self.central_data.index,
                     self.central_data["mean"],
                     [list(self.central_data["10%"]),
                      list(self.central_data["90%"])],
                     fmt='o',
                     capsize=10)
        self.plot_points(self.central_data.index,
                         self.central_data["min"])
        self.plot_points(self.central_data.index,
                         self.central_data["max"])
        self.plot_lines(self.central_data["25%"],
                        self.central_data["75%"])
        self.plot_median(self.central_data["50%"])
        plt.grid(ls="--",
                 color="#000000",
                 alpha=0.5,
                 axis="y")
        plt.show()

    def plot_points(self, x=[], y=[], marker="+"):
        plt.scatter(x, y,
                    color="#000000",
                    marker=marker)

    def plot_median(self, median_list=[]):
        for i, median in enumerate(median_list):
            plt.plot([i-self.length, i+self.length], [median, median],
                     color="#000000",
                     lw=2)

    def plot_lines(self, percentil_25_list=[], percentil_75_list=[]):
        i = 0
        for percentil_25, percentil_75 in zip(percentil_25_list,
                                              percentil_75_list):
            values = [
                [[i-self.length, i-self.length], [percentil_25, percentil_75]],
                [[i+self.length, i+self.length], [percentil_25, percentil_75]],
                [[i-self.length, i+self.length], [percentil_25, percentil_25]],
                [[i-self.length, i+self.length], [percentil_75, percentil_75]],
            ]
            for value in values:
                x, y = value
                plt.plot(x, y,
                         color="#000000")
            i += 1


def read_data(path="", file=""):
    """
    Lectura de los datos
    """
    data = pd.read_csv("{}{}".format(path,
                                     file))
    data = format_data(data)
    data = all_data_to_one_year(data)
    data = clean_data(data)
    return data


def format_data(data=pd.DataFrame()):
    """
    Formateo de los datos, indice con el estandar 
    de fecha, datos de W/m2 a IUV y eliminacion 
    de la columna de desviacion estandar.
    """
    data.index = pd.to_datetime(data["Dates"])
    data["Max"] = data["Max"]*40
    data = data.drop("std", 1)
    return data


def all_data_to_one_year(data=pd.DataFrame()):
    """
    """
    data["Dates"] = "2000"+data["Dates"].astype(str).str[4:]
    return data


def clean_data(data=pd.DataFrame()):
    """
    """
    data = data[data.index >= "2000-01-01"]
    data = data[data.index < "2020-01-01"]
    data.index = pd.to_datetime(data["Dates"])
    data = data.drop("Dates", 1)
    return data


def obtain_month_names():
    months = []
    for i in range(1, 13):
        date = datetime.datetime(2000, i, 1)
        month = date.strftime("%b")
        month = month_name_spanish_to_english(month)
        months.append(month)
    return months


def month_name_spanish_to_english(month=""):
    month_names = {
        "ene": "Jan",
        "abr": "Apr",
        "ago": "Aug",
        "dic": "Dec",
    }
    try:
        name = month_names[month]
    except:
        name = month.capitalize()
    return name


parameters = {
    "path data": "../Data/",
    "file data": "Max_Monthly_UVB.csv",
    "file tendency": "Central_tendency_monthly_data.csv",
}
data = read_data(parameters["path data"],
                 parameters["file data"])
data_box = data_boxes()
data_box.fill_data(data)
print(data_box.data_per_month.to_csv("data.csv",
                                     float_format="%.3f"))
# plt.boxplot(data_box.data_per_month.dropna())
# plt.ylim(0, 15)
# plt.show()
# boxes = plot_boxes(data=data_box.data_per_month,
#                    path=parameters["path data"],
#                    filename=parameters["file tendency"])
