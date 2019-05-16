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
from machine import Pin, ADC, I2C
import dht
from bmp180 import BMP180
import adafruit_sgp30

def leer_so2(pin_adc):
    """ Esta funcion es para leer los
    datos del sensor ULPSM-SO2"""
    """ Lectura del canal analogico """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    Vo = adc.read()*3.3/1024
    """ Conversion del voltaje a ppm"""
    if Vo == 0 or Vo<1.58877:
        ppm = 0
    else:
        M = 0.0494
        ppm = 1/M*(Vo-1.58877)
    return ppm

def leer_sgp30(scl_pin, sda_pin):
    """ esta funcion es para leer los datos del sensor
    sgp30 y retorna+
    CO2 en ppm
    TVOC en ppb"""
    i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    co2eq, tvoc = sgp30.iaq_measure()
    return co2eq, tvoc

def leer_dato_uv(pin_adc):
    """ Esta funcion es para leer los
    datos provenientes de los canales del ADC
    ademas esta la caracterizacion del sensor UV ML8511
    caracterizacion y = 0.1625x + 1.0
    x = (y - 1.0)/0.1625  mW/cm^2
    """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    y = adc.read()*3.3/1024
    if y < 1:
        x = 0
    else:
        x = (y-1.0)/0.1625
    return x

def leer_polvo(DPIN, APIN):
    """Definici0n de pines
    para el sensor de polvo GP2Y1010AU0F
    """
    p13 = Pin(DPIN, Pin.OUT)
    adc = ADC(Pin(APIN))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    #proceso de lectura para el sensor
    p13.off()
    utime.sleep_us(280)
    V1 = adc.read()*3.3/1024
    utime.sleep_us(40)
    p13.on()
    utime.sleep_us(9680)  
    dust_density = 0.17*V1-0.1
    return dust_density

def leer_MQ(pin_adc, A, b ,Ro):
    """ Esta funcion es para leer los
    datos de los sensores MQ que tienen un comportamiento
    ppm = ARo/Rs**(1/b)"""
    Rl = 1000 # Ohms
    Vref = 5  # Volts
    """ Lectura del canal analogico """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    Vo = adc.read()*3.3/1024
    """ Conversion del voltaje a ppm"""
    if Vo == 0:
        ppm = 0
    else:
        Rs = Rl*(Vref-Vo)/Vo
        ppm = (A*Ro/Rs)**(1/b)
    return ppm

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

def sensado():
    """Esta funcion se encarga de recolectar los datos de los sensores
    y enviarlos a la API creada
    """
    IP_SERVER = "34.74.6.16"

    """definicion de pines """
    # pin_MQ7 = 36
    # pin_MQ9 = 39 
    # pin_MQ131 = 34
    # pin_dht22 = 32
    # Apin_ML8511 = 33
    # pin_sda_sgp30 = 25
    # pin_scl_sgp30 = 26
    # pin_scl_bmp180 = 14
    # pin_sda_bmp180 = 27
    # pin_MQ4 = 35
    # Dpin_polvo = 13
    # Apin_polvo = 0
    # pin_MiCs2714 = 4
    pin_ULPSM = 15


    """sensado de variables"""
    fecha = utime.localtime()
    
    # temperatura, humedad = leer_temp_hum(pin_dht22) #leer datos del sensor DHT22
    # presion = leer_presion(pin_scl_bmp180,pin_sda_bmp180)#leer datos del sensor BMP180
    # luz_uv = leer_dato_uv(Apin_ML8511)
    """sensores de gas"""
    # sensor MQ7
    # A = 14.90 
    # b = 0.13  
    # Ro = 100 
    # ppm_mq7 = leer_MQ(pin_MQ7, A, b, Ro)
    # print("lpg {} ppm".format(ppm_mq7))

    #sensor MQ131
    # A = 3.12 
    # b = 0.38  
    # Ro = 100 
    # ppm_mq131 = leer_MQ(pin_MQ131, A, b, Ro)
    # print("O3 {} ppm".format(ppm_mq131))

    #sensor MQ4
    # A = 12.91 # de acuerdo a la curva del datasheet
    # b = 0.37  # de acuerdo a la curva del datasheet
    # Ro = 1000 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
    # ppm_mq4 = leer_MQ(pin_MQ4,A,b,Ro)
    # print("CH4 {} ppm".format(ppm_mq4))

    #sensor MQ9
    # A = 29.63 # de acuerdo a la curva del datasheet
    # b = 0.53  # de acuerdo a la curva del datasheet
    # Ro = 100 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
    # ppm_mq9 = leer_MQ(pin_MQ9, A, b, Ro)
    # print("CO {} ppm".format(ppm_mq9))

    #Sensor de polvo
    # dust_density=leer_polvo(Dpin_polvo,Apin_polvo)
    # print("dust_density {} mg/m^3 ". format(dust_density))

    #sensor sgp30 CO2 y tvoc
    # co2eq, tvoc = leer_sgp30(pin_scl_sgp30,pin_sda_sgp30)

    # sensor MiCs-2714
    # A = 6.68
    # b = 1
    # Ro = 100
    # ppm_no2 = leer_MQ(pin_MiCs2714,A,b,Ro)

    """envio de datos a la API"""
    # enviar_API("http://"+IP_SERVER+"/app_praes/temperatura/", fecha, temperatura, 1) # envio temperatura al sensor DHT22
    # enviar_API("http://"+IP_SERVER+"/app_praes/humedad/", fecha, humedad, 1) # envio humedad al sensor DHT22
    # enviar_API("http://"+IP_SERVER+"/app_praes/presion-atmosferica/", fecha, presion, 2) # envio humedad al sensor BMP180
    # enviar_API("http://"+IP_SERVER+"/app_praes/luz-uv/", fecha, luz_uv, 4) # envio humedad al sensor ML8511

    # enviar_API("http://"+IP_SERVER+"/app_praes/metano-propano-co/", fecha, ppm_mq7, 11) # envio humedad al sensor MQ7 
    # enviar_API("http://"+IP_SERVER+"/app_praes/o3/", fecha, ppm_mq131, 10) # envio humedad al sensor MQ131
    # enviar_API("http://"+IP_SERVER+"/app_praes/ch4/", fecha, ppm_mq4, 6) # envio humedad al sensor MQ4
    # enviar_API("http://"+IP_SERVER+"/app_praes/co/", fecha, ppm_mq9, 5) # envio humedad al sensor MQ4
    # enviar_API("http://"+IP_SERVER+"/app_praes/polvo/", fecha, dust_density, 7) # envio humedad al sensor GP2Y1010AU0F
    # enviar_API("http://"+IP_SERVER+"/app_praes/co2/", fecha, co2eq, 3) # envio dato al sensor SGP30
    # enviar_API("http://"+IP_SERVER+"/app_praes/material-organico/", fecha, tvoc, 3) # envio dato al sensor SGP30
    # enviar_API("http://"+IP_SERVER+"/app_praes/no2/", fecha, ppm_no2, 9) # envio dato al sensor Mics-2714 NO2

    # Sensor SO2 lo dejo al final de todo ya que requiere de un tiempito para dar respuesta
    ppm_so2 = leer_so2(pin_ULPSM)
    enviar_API("http://"+IP_SERVER+"/app_praes/so2/", fecha, ppm_so2, 8) # envio dato al sensor ULPSM


def sub_cb(topic, msg):
    """ Esta es la funcion que se encarga de interpretar todas las 
    acciones enviadas por MQTT, es decir, el menu dado por 
    Control KIT ambiental
    """
    p9 = Pin(9, Pin.OUT) #pin para LED indicador
    
    if msg == b"1 medicion":
        sensado()
        """encender led para indicar que la comunicacion ha sido correcta"""        
        p9.on()  
        time.sleep(500e-3)
        p9.off()
        time.sleep(500e-3)

    if msg == b"30 segundos":
        timming = 0
        t1 = time.time()
        while timming<=30:
            sensado()
            p9.on()  
            time.sleep(100e-3)
            p9.off()
            time.sleep(100e-3)
            t2 = time.time()
            timming = t2-t1

    if msg == b"1 minuto":
        timming = 0
        t1 = time.time()
        while timming<=60:
            sensado()
            p9.on()  
            time.sleep(100e-3)
            p9.off()
            time.sleep(100e-3)
            t2 = time.time()
            timming = t2-t1

    if msg == b"5 minutos":
        timming = 0
        t1 = time.time()
        while timming<=60:
            sensado()
            p9.on()  
            time.sleep(100e-3)
            p9.off()
            time.sleep(100e-3)
            t2 = time.time()
            timming = t2-t1

                
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



