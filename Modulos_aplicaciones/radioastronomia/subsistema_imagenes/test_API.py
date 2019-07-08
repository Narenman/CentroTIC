import requests


files = {'imagen': open("stars2.jpg", "rb")}
pyload = {'region': 1}
url = "http://127.0.0.1:8000/radioastronomia/album-imagenes"
r = requests.post(url, data=pyload, files=files)
print(r.text)
print(r.status_code)
r.close()