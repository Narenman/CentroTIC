import urequests
import utime 
import machine
import ujson

def enviar_API(url, fecha, valor, sensor):
    """ esta funcion se encarga de enviar los datos a la API"""
    date = str(fecha[0])+"-"+str(fecha[1])+"-"+str(fecha[2])+" "+str(fecha[3])+":"+str(fecha[4])+":"+str(fecha[5])
    pyload = {
        "fecha": date,
        "valor": valor,
        "sensor": sensor
    }
    r = urequests.post(url, json=pyload, headers={"Authorization": " Token 9a74a56ab171cacdee5654cfc2ebd126694e1bf0",
                                                    "Content-Type": "application/json"})
    print(r.content)
    print(r.status_code)
    r.close()


fecha = utime.localtime()
url = "http://34.74.6.16/app_praes/temperatura/"
sensor = 1
valor = 1000
enviar_API(url, fecha, valor, sensor)
