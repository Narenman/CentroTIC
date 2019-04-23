""" Para conectarse a una red WiFi
en este caso la red tiene:
SSID: radiogis
password: radio.1359"""
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('radiogis', 'radio.1359')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
do_connect()

"""para configurar la hora de la ESP32
con la hora del servidor"""
import utime
from urequests import urequests
import ujson
from machine import RTC
r = urequests.get("http://34.73.25.149/app_praes/hora-local/")
tm = ujson.loads(r.text)
tm = tm["GMT-5"]
tm = tuple(tm[0:8])
rtc = RTC()
rtc.datetime(tm)

"""Ejecuta el programa principal de la tarjeta
"""
import monitoreo_esp32