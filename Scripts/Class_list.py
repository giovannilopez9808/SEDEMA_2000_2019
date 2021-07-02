from Functions import *
import pandas as pd
import os


class OMI_data_set:
    def __init__(self, path="", name=""):
        self.path = path
        self.name = name
        self.read_data()

    def read_data(self):
        """
        Lectura de los datos de OMI
        #### inputs
        path -> direccion donde se encuentran los datos

        name -> nombre del archivo
        """
        # Lectura cruda de los datos
        data = pd.read_csv("{}UVI_{}.csv".format(self.path,
                                                 self.name),
                           index_col=0)
        # Formato de fecha a los datos
        self.data = self.format_data(data)

    def format_data(self, data=pd.DataFrame()):
        """
        Formato de fecha en el indice del dataframe
        """
        data.index = pd.to_datetime(data.index)
        return data


class SEDEMA_data_set:
    def __init__(self, path="", type_name="UVB"):
        self.path = path
        self.type = type_name
        self.resize = {"UVA": 10,
                       "UVB": 0.0583*40, }
        self.resize = self.resize[type_name]
        self.read_data()

    def read_data(self):
        """
        Lectura de los datos de la SEDEMA
        #### inputs
        path -> direccion donde se encuentran los datos

        resize -> valor para convertir los datos a UVI
        """
        # Listado de los archivos de la SEDEMA
        files = sorted(os.listdir(self.path))
        # Seleccionar unicamente los de UVB
        files = self.select_files(files=files)
        # Ciclo para reunir todos los archivos en un solo dataframe
        for i, file in enumerate(files):
            if i == 0:
                # Lectura de los datos de la SEDEMA
                self.data = self.read_data_each_file(self.path,
                                                     file)
            else:
                # Lectura de los datos de la SEDEMA
                data_year = self.read_data_each_file(self.path,
                                                     file)
                # Union de todos los dataframe en uno solo
                self.data = self.data.append(data_year)
        # Redimensionar los datos UVI
        self.data["value"] = self.data["value"]*self.resize

    def select_files(self, files=[]):
        """
        Descarta los archivos dependiendo si contienen un nombre en especifico
        #### inputs
        files -> listado de los archivos sin filtrar
        """
        files_type = []
        for file in files:
            # Filtrado
            if self.type in file:
                files_type.append(file)
        return files_type

    def read_data_each_file(self, path="", name=""):
        """
        Lectura de cada archivo de datos de la SEDEMA
        """
        # Lectura cruda de los datos
        data = pd.read_csv("{}{}".format(path,
                                         name),
                           index_col=0)
        # Formateo del dataframe
        data = self.format_data(data)
        return data

    def format_data(self, data=pd.DataFrame()):
        """
        Elimina columnas innecesarias y realiza el formato de fecha al indice del dataframe
        """
        # Formato de fecha al indice
        data.index = pd.to_datetime(data.index)
        # Eliminacion de columnas inncesarias
        data = data.drop(["parameter",
                          "unit",
                          "cve_station"],
                         1)
        return data
