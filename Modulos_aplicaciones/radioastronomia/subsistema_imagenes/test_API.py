import requests


# files = {'imagen': open("stars2.jpg", "rb")} #para cargar la imagen
files = {'imagen': open("aurora.mp4", "rb")} #para cargar un video

pyload = {'region': 1}
url = "http://127.0.0.1:8000/radioastronomia/album-imagenes"
r = requests.post(url, data=pyload, files=files)
print(r.text)
print(r.status_code)
r.close()