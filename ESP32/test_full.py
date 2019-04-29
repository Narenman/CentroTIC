"""
Este archivo contiene las funciones MQTT,  enviar a traves de la API
La URL especificada y la funcion para leer el dato proveniente del ADC.
"""
from urequests import urequests
import utime 
from machine import Pin
import machine
import time
from  umqtt.simple import MQTTClient
import ubinascii
import micropython
from machine import ADC
import dht


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
    """ Esta funcion se encarga de enviar los datos
    a la API para que sean almacenados en la base de datos
    de acuerdo a la url especificada.
    """
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
    # podria retornarse el status HTTP para indicar a un led que todo esta  bien

def leer_dato(pin_adc):
    """ Esta funcion es para leer los
    datos provenientes de los canales del
    ADC"""
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    adc_pot = adc.read()*3.0/1024
    return adc_pot

def sub_cb(topic, msg):
    """ Esta es la funcion que se encarga de interpretar todas las 
    acciones enviadas por MQTT, es decir, el menu dado por 
    Control KIT ambiental
    """
    if msg == b"ESP32-LED":

        temperatura, humedad = leer_temp_hum(32)
        print(temperatura)

        #envio de datos a la API
        fecha = utime.localtime()
        url = "http://34.73.25.149/app_praes/temperatura/"
        sensor = 1
        valor = leer_dato(36)
        enviar_API(url, fecha, valor, sensor)

        #encender led para indicar que la comunicacion ha sido correcta        
        p9 = Pin(9, Pin.OUT)   
        for i in range(10):
            p9.on()  
            time.sleep(200e-3)
            p9.off()
            time.sleep(200e-3)

                
# Default MQTT server to connect to
SERVER = "34.73.25.149"
TOPIC = b"UIS/LP/213"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
print("client id {}".format(CLIENT_ID))
client = MQTTClient(client_id=CLIENT_ID, server=SERVER, port=1883, user="pi", password="raspberry")
client.set_callback(sub_cb)
client.connect()
client.subscribe(TOPIC)
print("suscripcion exitosa")
try: 
    while True:
        micropython.mem_info()
        client.wait_msg()
finally:
    client.disconnect()



