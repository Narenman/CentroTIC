import requests
import json

r = requests.get("http://127.0.0.1:8000/app_praes/hora-local/")
tm = json.loads(r.text)
tm = tm["GMT-5"]
print(tm)
# print(type(tm[0]))
# tm = (tm[0:4], tm[5:7], tm[8:10], tm[11:13], tm[14:16], tm[17:19], '000', '0')

import time
tz = time.localtime()
timez = {"tz": tz}
print(timez)