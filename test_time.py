import requests
import json

r = requests.get("http://34.73.25.149/app_praes/hora-local/")
tm = json.loads(r.text)
tm = tm["GMT-5"][0:7]
print(tm)