import dht
from machine import Pin

def leer_temp_hum(pin):
    """ esta funcion es para leer los datos asociados
    al sensor DHT11, sin embargo, la libreria funciona para otros sensores
    como el DHT22.
    La funcion retorna valores de temperatura y humedad
    """
    d = dht.DHT22(Pin(pin, Pin.IN, Pin.PULL_UP))
    d.measure()
    return d.temperature(), d.humidity()

temperatura, humedad = leer_temp_hum(32)
print("temperatura {}".format(temperatura))
print("humedad {}".format(humedad))
