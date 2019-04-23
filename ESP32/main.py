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
        wlan.connect('AndroidAP', 'mzwj9860')
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
tm = (int(tm[0:4]), int(tm[5:7]), int(tm[8:10]), int(tm[11:13]), int(tm[14:16]), int(tm[17:19]), 000, -5)
rtc = RTC()
rtc.datetime(tm)

"""Ejecuta el programa principal de la tarjeta
"""
import monitoreo_esp32