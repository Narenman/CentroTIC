import os
import json

def get_coordinates():
    """Esta funcion se encarga de extraer las coordenadas del gps
    del equipo E310 """
    os.system("gpspipe -w -n 10 | grep TPV >coordenadas.txt")
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    f = open(DIR_PATH+"/coordenadas.txt", "r")
    latitud = []
    longitud = []
    for line in f:
        dat = json.loads(line)
        latitud.append(dat["lat"])
        longitud.append(dat["lon"])

    lat = 0
    lon = 0
    for k in range(len(latitud)):
        lat+= latitud[k]
        lon+= longitud[k]
    lat = lat/len(latitud)
    lon = lon/len(latitud)

    return lat, lon

if __name__ == "__main__":
    latitud, longitud = get_coordinates()
    print("latitud: {}\nlongitud: {}".format(latitud, longitud))