import bme280
import requests
import json
import time

def bme280x():
    """Se encarga de realizar las lecturas del sensor digital
    bme280 para medir variables temperatura, humedad y presion """
    temperature,pressure,humidity = bme280.readBME280All()
    return temperature, pressure, humidity


global direccionIP
direccionIP = "192.168.0.103:8000"
ubicacion = 45
kit = 1
APIusername="mario"
APIpassword="mario"


def getToken(username, password):
    """Esta funcion se encarga de consultar el token de acuerdo al usuario
    y contrasena para la API """
    data = {
    "username": username,
    "password": password}
    URL = "http://"+direccionIP+"/app_praes/token/"
    r = requests.post(URL, data=data)
    print("HTTP status token {}".format(r.status_code))
    token = json.loads(r.content)
    # print(token["token"])
    return token

def comunicacionAPI(URL,valor, ubicacion, kit):
    """ este metodo es para comunicarse con la base 
    de datos a traves de API REST
    """
    data = {"valor": valor,
            "kit_monitoreo": kit,
            "ubicacion": ubicacion}
    token = getToken(APIusername, APIpassword)
    headers={"Authorization":"Token "+token["token"]} 
    r = requests.post(URL, data=data, headers=headers)
    if r.status_code==200 or r.status_code==201:
        print("HTTP status API. {}".format(r.status_code))
        r.close()
    else:
        print("Bad request {}".format(r.status_code))



URL = "http://"+direccionIP+"/app_praes/temperatura/"
for i in range(20):
    temperature, pressure, humidity = bme280x()
    comunicacionAPI(URL, temperature, ubicacion, kit)
    time.sleep(0.5)