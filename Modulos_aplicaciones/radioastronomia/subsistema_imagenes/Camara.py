import requests
import json
import getOculusimage
import time
import threading
import os
import cv2
from datetime import datetime

class CamaraAllsky():
    def __init__(self, IP, usernameAPI, passwordAPI):
        self.IP = IP
        self.usernameAPI = usernameAPI
        self.passwordAPI = passwordAPI

    def clean(self,):
        os.system("rm -r imagenes/jpgs/*.jpg")
        os.system("rm -r imagenes/fits/*.fit")
        print("Archivos previos borrados")

    def get_frames(self, Nframes, time1):
        for i in range(Nframes):
            time.sleep(time1)
            os.system("python3 getOculusimage.py")
    
    def time_lapse(self,):
        """Extrae los archivos de la carpeta frames y los organiza por
        fecha de adquisicion """
        frames = os.listdir("imagenes/jpgs")
        frames = list(map(lambda dates: datetime.strptime(dates.replace('.jpg',''), '%Y-%m-%d %H:%M:%S.%f'), frames))
        frames = sorted(frames)
        frames = list(map(lambda files: str(files)+".jpg", frames))

        img_array = []
        for f in frames:
            img = cv2.imread("imagenes/jpgs/"+f)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        path_file = datetime.now()
        writer = cv2.VideoWriter("timelapses/"+str(path_file)+".mp4",cv2.VideoWriter_fourcc(*'mp4v'), 10, size)
        for i in range(len(img_array)):
            writer.write(img_array[i])
        writer.release()
        print("timelapse creado")
        return "timelapses/"+str(path_file)+".mp4"

        #comunicacion con la API
    def getToken(self):
        """Esta funcion se encarga de consultar el token de acuerdo al usuario
        y contrasena para la API """
        data = {
        "username": self.usernameAPI,
        "password": self.passwordAPI}
        URL = "http://"+self.IP+"/app_praes/token/"
        r = requests.post(URL, data=data)
        print("HTTP status token {}".format(r.status_code))
        token = json.loads(r.content)
        # print(token["token"])
        return token["token"]

    def camaraAPI(self, region):
        """ este metodo es para iniciar la comunicacion donde la base de datos
        y registrar las mediciones, las entradas son:
        * URL: es la direccion de la API sin colocar la IP, por ejemplo: /radioastronomia/estacion-monitoreo
        * valores: es un json que contiene las lecturas
        * region: es el id de la region donde se registra la medicion
        """

        ruta = self.time_lapse()
        files = {'imagen': open(ruta, "rb")} #para cargar un video
        data = {"region": region}
        
        token = self.getToken()
        headers={"Authorization":"Token "+token}
        URL = "http://"+self.IP+"/radioastronomia/album-imagenes"
        r = requests.post(URL, data=data, files=files, headers=headers)

        if r.status_code==200:
            print("HTTP status ok. {}".format(r.status_code))
            r.close()
        else:
            print(r.status_code)
    

if __name__ == "__main__":
    Nframes = 10
    time1 = 0.1
    IP = "192.168.0.113:8000"
    usernameAPI = "mario"
    passwordAPI = "mario"
    region = 1
    camara = CamaraAllsky(IP,usernameAPI, passwordAPI)
    camara.clean()
    camara.get_frames(Nframes, time1)
    # camara.time_lapse()
    camara.camaraAPI(region)