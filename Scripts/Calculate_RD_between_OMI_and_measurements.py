import matplotlib.pyplot as plt
from Class_list import *


def obtain_xticks(date_initial="2005-01-01", date_final="2019-12-31"):
    """
    obtiene los ticks labels dependiendo del periodo en donde se hara el analisis
    """
    year_initial = int(date_initial[0:4])
    year_final = int(date_final[0:4])
    years = [year for year in range(year_initial, year_final+2)]
    dates = [pd.to_datetime("{}-01-01".format(year)) for year in years]
    return dates, years


parameters = {
    "path data": "../Data/",
    "path graphics": "../Graphics/",
    "OMI column": "CSUVindex",
    "path SEDEMA data": "../Data/SEDEMA_Data/Radiation/",
    "wavelength": "UVB",
    "Year initial": "2005-01-01",
    "Year final": "2019-12-31",
    "fontsize": 14,
}
# Lectura de los datos de OMI
OMI_data = OMI_data_set(parameters["path data"],
                        parameters["OMI column"])
# Calculo del promedio mensual
OMI_monthly_mean = obtain_monthly_mean(OMI_data.data)
# Seleccionar datos que estan dentro del periodo
OMI_monthly_mean = select_data(data=OMI_monthly_mean,
                               date_initial=parameters["Year initial"],
                               date_final=parameters["Year final"])
monthly_mean = pd.DataFrame(index=OMI_monthly_mean.index)
monthly_mean["OMI"] = OMI_monthly_mean["CSUVindex"]
# Lectura de los datoa de SEDEMA
SEDEMA_data = SEDEMA_data_set(path=parameters["path SEDEMA data"],
                              type_name=parameters["wavelength"])
SEDEMA_data.data = obtain_daily_maximum(SEDEMA_data.data)
# Calculo del promedio mensual
SEDEMA_monthly_mean = obtain_monthly_mean(SEDEMA_data.data)
# Seleccionar datos que estan dentro del periodo
SEDEMA_monthly_mean = select_data(data=SEDEMA_monthly_mean,
                                  date_initial=parameters["Year initial"],
                                  date_final=parameters["Year final"])
monthly_mean["SEDEMA"] = SEDEMA_monthly_mean["value"]
# Calculo de la RD
monthly_mean["RD"] = (monthly_mean["OMI"] -
                      monthly_mean["SEDEMA"])/monthly_mean["SEDEMA"]*100
monthly_mean.to_csv("{}Monthly_mean_RD.csv".format(parameters["path data"]),
                    float_format="%.2f")
print("La diferencial relativa promedio es {:.2f}".format(
    monthly_mean["RD"].mean()))
# Inicio del ploteo de los datos
dates, years = obtain_xticks(parameters["Year initial"],
                             parameters["Year final"])
plt.figure(figsize=(10, 4))
plt.subplots_adjust(left=0.085,
                    bottom=0.13,
                    right=0.971,
                    top=0.926)
plt.xlabel("Years",
           fontsize=parameters["fontsize"])
plt.xlim(pd.to_datetime(parameters["Year initial"]),
         pd.to_datetime(parameters["Year final"]))
plt.xticks(dates, years,
           fontsize=parameters["fontsize"])
plt.ylabel("Percentage difference",
           fontsize=parameters["fontsize"])
plt.ylim(0, 120)
plt.yticks([tick for tick in range(0, 120, 10)],
           fontsize=parameters["fontsize"])
plt.scatter(monthly_mean.index, monthly_mean["RD"],
            c="#9D2449")
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.savefig("{}Monthly_mean_RD.png".format(parameters["path graphics"]),
            dpi=400)
