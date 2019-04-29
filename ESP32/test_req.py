from urequests import urequests
import utime 
import dht
import machine

def leer_temp_hum(pin):
    """ esta funcion es para leer los datos asociados
    al sensor DHT11, sin embargo, la libreria funciona para otros sensores
    como el DHT22.
    La funcion retorna valores de temperatura y humedad
    """
    d = dht.DHT11(machine.Pin(pin))
    d.measure()
    return d.temperature(), d.humidity()


def enviar_API(url, fecha, valor, sensor):

    date = str(fecha[0])+"-"+str(fecha[1])+"-"+str(fecha[2])+" "+str(fecha[3])+":"+str(fecha[4])+":"+str(fecha[5])
    pyload = {
        "fecha": date,
        "valor": valor,
        "sensor": sensor
    }
    r = urequests.post(url, json=pyload, headers={"Authorization": " Token d2865cc229825bd3b05d765f11f21b6b80c0fff6"})
    print(r.content)
    print(r.status_code)
    r.close()


fecha = utime.localtime()
temperatura, humedad = leer_temp_hum(32)

print("temperatura ", temperatura)
print("humedad ", humedad)
url = "http://34.73.25.149/app_praes/temperatura/"
sensor = 2
valor = temperatura
enviar_API(url, fecha, valor, sensor)
