import machine
import time
from  umqtt.simple import MQTTClient
import ubinascii
import micropython
import urequests
from machine import Pin, ADC
import time
import ujson

def leer_MQ2(pin_adc):
    """ Lectura del canal analogico """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    Vo = adc.read()
    return Vo


def enviar_API(url, medicion, asociacion):
    """ Esta funcion se encarga de enviar los datos
    a la API para que sean almacenados en la base de datos
    de acuerdo a la url especificada.
    """
    pyload = {
        "medicion": medicion,
        "asociacion": asociacion
    }
    r = urequests.post(url, json=pyload, headers={"Content-Type": "application/json"})
    print(r.content)
    print(r.status_code)
    r.close()
    # podria retornarse el status HTTP para indicar a un led que todo esta  bien

def modo_nariz():
    pin_MQ7 = 36
    pin_MQ9 = 39 
    pin_MQ131 = 34
    pin_MQ4 = 35

    s1 = leer_MQ2(pin_MQ7)
    s2 = leer_MQ2(pin_MQ4)
    s3 = leer_MQ2(pin_MQ7)
    s4 = leer_MQ2(pin_MQ131)
    medicion = [s1,s2,s3,s4]
    
    return medicion


def sub_cb(topic, msg):
    dato = ujson.loads(msg)

    if dato["control"] == "modo-nariz":
        url = "http://34.74.6.16/app_praes/modo-nariz/"
        t1 = time.time()
        timming = 0
        while timming<=10:
            medicion = modo_nariz()
            asociacion = dato["asociacion"]
            enviar_API(url, medicion, asociacion)
            timming = time.time()-t1
            
# Default MQTT server to connect to
SERVER = "34.74.6.16"
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


#print(modo_nariz())