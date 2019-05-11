"""
Este archivo contiene las funciones MQTT,  enviar a traves de la API
La URL especificada y la funcion para leer el dato proveniente del ADC.
"""
from urequests import urequests
from  umqtt.simple import MQTTClient
import utime 
import time
import ubinascii
import micropython
import machine
from machine import Pin
from machine import ADC
from machine import I2C
import dht
from bmp180 import BMP180


def leer_presion(scl_pin, sda_pin):
    """ Lee la presion del sensor BMP180 """
    bus = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)  # create I2C peripheral at frequency of 400kHz
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

    temp = bmp180.temperature
    p = bmp180.pressure
    altitude = bmp180.altitude
    return p


def leer_temp_hum(pin):
    """ esta funcion es para leer los datos asociados
    al sensor DHT11, sin embargo, la libreria funciona para otros sensores
    como el DHT22.
    La funcion retorna valores de temperatura y humedad
    """
    d = dht.DHT22(Pin(pin, Pin.IN, Pin.PULL_UP))
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
    r = urequests.post(url, json=pyload, headers={"Authorization": " Token 9a74a56ab171cacdee5654cfc2ebd126694e1bf0"})
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

        temperatura, humedad = leer_temp_hum(32) #leer datos del sensor DHT22
        presion = leer_presion(14,27)#leer datos del sensor BMP180


        #envio de datos a la API
        fecha = utime.localtime()
        enviar_API("http://34.74.6.16/app_praes/temperatura/", fecha, temperatura, 2) # envio temperatura al sensor DHT22
        enviar_API("http://34.74.6.16/app_praes/humedad/", fecha, humedad, 2) # envio humedad al sensor DHT22
        enviar_API("http://34.74.6.16/app_praes/presion-atmosferica/", fecha, presion, 5) # envio humedad al sensor BMP180



        #encender led para indicar que la comunicacion ha sido correcta        
        p9 = Pin(9, Pin.OUT)   
        for i in range(10):
            p9.on()  
            time.sleep(200e-3)
            p9.off()
            time.sleep(200e-3)

                
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



