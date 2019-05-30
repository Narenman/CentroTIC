def do_connect():
    """ Para conectarse a una red WiFi
    en este caso la red tiene:
    SSID: radiogis
    password: radio.1359"""
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('radiogis', 'radio.1359')
        # wlan.connect('STEVEN', 'T1098739863')
        # wlan.connect('AndroidAP', 'mzwj9860')


        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
do_connect()

"""para configurar la hora de la ESP32
con la hora del servidor"""
import utime
import urequests
import ujson
from machine import RTC
r = urequests.get("http://34.74.6.16/app_praes/hora-local/")
tm = ujson.loads(r.text)
tm = tm["GMT-5"]
print(tm)
tm = (int(tm[0:4]), int(tm[5:7]), int(tm[8:10]), int(tm[11:13]), int(tm[14:16]), int(tm[17:19]), 000, -5)
rtc = RTC()
rtc.datetime(tm)
print("hora configurada {}".format(utime.localtime()))
"""Ejecuta el programa principal de la tarjeta
"""
import test_full