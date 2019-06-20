import requests
import json


pyload = {
    "espectro_IQ": [[100,200],[300,600]],
    "frec_central": 96000000,
    "dispositivo": 1
}

headers={"Authorization": " Token d2865cc229825bd3b05d765f11f21b6b80c0fff6"}

r = requests.put("http://127.0.0.1:8000/bloqueadores/espectro/1", json=pyload)
print(r.text)
print(r.status_code)
r.close()