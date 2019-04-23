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
