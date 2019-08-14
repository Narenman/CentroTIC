import requests
import json

data = {
    "username": "mario",
    "password": "mario"
  }

URL = "http://127.0.0.1:8000/app_praes/token/"
r = requests.post(URL, data=data)
print("HTTP status {}".format(r.status_code))
token = json.loads(r.content)
print(token["token"])