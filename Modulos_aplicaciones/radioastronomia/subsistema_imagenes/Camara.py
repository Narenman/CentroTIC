import requests
import json


class CamaraAllsky():

    def __init__(self,direccionIP, APIusername, APIpassword):
        self.direccionIP = direccionIP
        self.APIusername = APIusername
        self.APIpassword = APIpassword

    #comunicacion con la API
    def getToken(self):
        """Esta funcion se encarga de consultar el token de acuerdo al usuario
        y contrasena para la API """
        data = {
        "username": self.APIusername,
        "password": self.APIpassword}
        URL = "http://"+self.direccionIP+"/app_praes/token/"
        r = requests.post(URL, data=data)
        print("HTTP status token {}".format(r.status_code))
        token = json.loads(r.content)
        # print(token["token"])
        return token["token"]

    def camaraAPI(self, ruta, region):
        """ este metodo es para iniciar la comunicacion donde la base de datos
        y registrar las mediciones, las entradas son:
        * URL: es la direccion de la API sin colocar la IP, por ejemplo: /radioastronomia/estacion-monitoreo
        * valores: es un json que contiene las lecturas
        * region: es el id de la region donde se registra la medicion
        """
        files = {'imagen': open(ruta, "rb")} #para cargar un video
        data = {"region": region}
        
        token = self.getToken()
        headers={"Authorization":"Token "+token}
        URL = "http://"+self.direccionIP+"/radioastronomia/album-imagenes"
        r = requests.post(URL, data=data, files=files, headers=headers)

        if r.status_code==200:
            print("HTTP status ok. {}".format(r.status_code))
            r.close()
        else:
            print(r.status_code)
    

if __name__ == "__main__":
    direccionIP = "192.168.0.102:8000"
    APIusername = "mario"
    APIpassword = "mario"
    region = 8
    ruta = "/home/pi/radioastronomia/Camara/videos/observacion"

    camara = CamaraAllsky(direccionIP, APIusername, APIpassword)
    videos = ["1.mp4", "2.mp4","3.mp4","4.mp4"]
    for vid in videos:
        camara.camaraAPI(ruta+vid, region)