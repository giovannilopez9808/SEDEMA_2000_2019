from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import datetime
import locale
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        pass


def obtain_month_names():
    names = []
    for i in range(1, 13):
        date = datetime.date(2000, i, 1)
        names.append(date.strftime("%b"))
    return names


def obtain_date_and_hour(date):
    hour = int(date[11:13])
    day = int(date[0:2])
    month = int(date[3:5])
    year = int(date[6:10])
    date = datetime.date(year, month, day)
    return date, hour


def obtain_day_consecutive(date):
    conseday = (date-datetime.date(date.year, 1, 1)).days
    if conseday > 364:
        conseday = 364
    return conseday


def conseday_to_date(conseday, year):
    date = datetime.date(year, 1, 1)+datetime.timedelta(days=conseday)
    return date


def date_formtat_mmdd(date):
    date = date.strftime("%m-%d")
    return date


def find_location(name, data_list):
    for loc, elements in enumerate(data_list):
        if name == elements:
            return loc


def date2yymmdd(date):
    year, month, day = str(date).split("-")
    year = year[2:4]
    return year+month+day


def obtain_date_from_filename(name):
    year = int("20"+name[0:2])
    month = int(name[2:4])
    day = int(name[4:6])
    date = datetime.date(year, month, day)
    return date


def forceAspect(ax, aspect):
    im = ax.get_images()
    extent = im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)


def colormap_UVI():
    colors = [  # (0, 0, 0),
        (58/255, 156/255, 43/255),
        (152/255, 196/255, 8/255),
        (1, 244/255, 0),
        (1, 211/255, 0),
        (246/255, 174/255, 0),
        (239/255, 131/255, 0),
        (232/255, 97/255, 5/255),
        (255/255, 34/255, 34/255),
        (230/255, 42/255, 20/255),
        (165/255, 0/255, 0/255),
        (118/255, 8/255, 104/255),
        (118/255, 46/255, 159/255),
        (150/255, 53/255, 188/255),
        (156/255, 92/255, 188/255),
        (184/255, 150/255, 235/255),
        (198/255, 198/255, 248/255)]
    n_bin = len(colors)
    cmap_name = "UV_Index"
    cm = LinearSegmentedColormap.from_list(cmap_name,
                                           colors,
                                           N=n_bin)
    return cm
