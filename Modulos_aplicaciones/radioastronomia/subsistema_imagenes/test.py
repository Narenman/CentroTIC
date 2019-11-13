import requests
import json

def estadocamara(dat):
    """esta funcion se encarga de actualizar el estado
    de la estacion metereologica """
    URL = "http://"+IP+"/radioastronomia/estado/camara/1"
    pyload = {"camara": dat}
    r = requests.put(URL, data=pyload)
    dato = r.text
    estado = json.loads(dato)
    print("Estacion {}".format(dato))
    print("HTTP status code {} consulta estado SDR".format(r.status_code))
    r.close()

if __name__ == "__main__":
    global IP
    IP = "192.168.0.113:8000"
    estadocamara(False)