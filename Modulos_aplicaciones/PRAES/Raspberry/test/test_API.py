import requests
import json

def send_API(URL,valor, ubicacion):
    """ este metodo es para iniciar la comunicacion donde la base de datos
    retorna el init resp
    """
    data = {"valor": valor,
            "sensor": 1,
            "ubicacion": ubicacion}
            
    headers={"Authorization":"Token 33565da4cc7e8394310dfa74160222e484b4fe6f"} 
    r = requests.post(URL, data=data, headers=headers)
    if r.status_code==200:
        print("HTTP status ok. {}".format(r.status_code))
        r.close()
    else:
        print(r.status_code)

if __name__ == "__main__":
    URL = "http://192.168.0.103:8000/app_praes/temperatura-agua/"
    valor = 20
    ubicacion = 1
    send_API(URL, valor, ubicacion)