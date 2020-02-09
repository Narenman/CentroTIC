"""para configurar la hora de la ESP32
con la hora del servidor"""

import utime
from urequests import urequests
import ujson
from machine import RTC

r = urequests.get("http://34.73.25.149/app_praes/hora-local/")
tm = ujson.loads(r.text)
tm = tm["GMT-5"]
# tm= tuple(tm[0:8])
tm = (int(tm[0:4]), int(tm[5:7]), int(tm[8:10]), int(tm[11:13]), int(tm[14:16]), int(tm[17:19]), 0, 113)
print(tm)
rtc = RTC()
rtc.datetime(tm)
print(utime.localtime())
