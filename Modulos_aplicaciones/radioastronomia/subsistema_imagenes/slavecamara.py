import paho.mqtt.publish as publish
import threading
import paho.mqtt.client as mqttClient
import requests
import time
import json
from Camara import CamaraAllsky

def getSDRstate():
    """esta funcion se encarga de actualizar el estado
    de la estacion metereologica """
    URL = "http://"+IP+"/radioastronomia/estado/1"
    r = requests.get(URL)
    dato = r.text
    estado = json.loads(dato)
    print("Estacion {}".format(dato))
    print("HTTP status code {} consulta estado SDR".format(r.status_code))
    r.close()
    return estado["activo"]


def manual(**accion):
    region = accion["region"]


def automatico(**accion):
    region = accion["region"]
    Nframes = 60
    time1 = 0.1

    camara = CamaraAllsky(IP,usernameAPI, passwordAPI)

    time.sleep(10)
    camara.estadocamara(True)
    sdr_stado = getSDRstate()
    camara.clean()

    while sdr_stado==True:
        camara.get_frames(Nframes, time1)
        sdr_stado = getSDRstate()
        time.sleep(1)
    
    camara.camaraAPI(region)
    camara.estadocamara(False)

# funciones auxiliares
class MQTTSuscriptor():
    def __init__(self, broker_address,
                       port,
                       usuario_broker,
                       contrasena_broker):
        self.broker_address = broker_address
        self.port = port
        self.usuario_broker = usuario_broker
        self.contrasena_broker = contrasena_broker
        self.client = mqttClient.Client() 
        self.client.username_pw_set(self.usuario_broker, password=self.contrasena_broker) 
        self.client.connect(self.broker_address, port=self.port)    

    def publishMQTT(self, topico, msg):
        """ Se encarga de establecer comunicacion
        MQTT con los dispositivos """
        publish.single(topico, msg, port=self.port, hostname=self.broker_address,
        auth={"username": self.usuario_broker, "password":self.contrasena_broker})

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("conexion exitosa con el broker")
        client.subscribe("radioastronomia/RFI")

    def on_message(self, client, userdata, message):
            accion = message.payload.decode() #es el mensaje enviado por el cliente
            accion = json.loads(accion)
            global stop_thread2, stop_thread3
            stop_thread3 = False
            stop_thread2 = False

            if accion["accion"] == "modo manual":
                print("modo manual seleccionado")
                """ Con esta instruccion el E310 sensa el espectro y envia los datos """
                # print(accion)
                #configuracion de variables provenientes del servidor
                region = accion["region"]

                #mensajes para controlador posicion
                kwargs = { "region": region}
                kwargs.update({"IP": broker_address, "port": port,
                   "username": usuario_broker, "password": contrasena_broker})
                #hilo controlador
                hilo2 = threading.Thread(target=manual, kwargs=kwargs)
                hilo2.start()
                # self.client.disconnect()

            if accion["accion"] == "modo automatico":
                # print(accion)
                print("Modo automatico seleccionado")
                region = accion["region"]
                
                kwargs = {"region": region}
                kwargs.update({"IP": broker_address, "port": port,
                   "username": usuario_broker, "password": contrasena_broker})
                hilo3 = threading.Thread(target=automatico, kwargs=kwargs)
                hilo3.start()
                # self.client.disconnect()
            
            if accion["accion"] == "detener":
                stop_thread3 = True
                stop_thread2 = True

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

    def __del__(self):
        self.client.disconnect()


def adquisicionRFI(**conf):
    #aca iba un while
    objmqtt = MQTTSuscriptor(broker_address=conf["IP"], port=conf["port"], usuario_broker=conf["username"],
                            contrasena_broker=conf["password"])
    objmqtt.comunicacionMQTT()

if __name__ == "__main__":
    global IP, IPbroker, usernameAPI, passwordAPI
    global stop_thread2, stop_thread3
    stop_thread2 = False
    stop_thread3 = False

    # conexion servidor web
    # IP = "35.243.199.245"
    IP = "192.168.0.113:8000"

    usernameAPI  = "mario"
    passwordAPI = "mario"
    # conexion broker
    broker_address ="35.243.199.245"
    port = 1883
    usuario_broker = "pi"
    contrasena_broker = "raspberry"

    
    kwargs_conf = {"IP": broker_address, "port": port,
                   "username": usuario_broker, "password": contrasena_broker}
    hilo1 = threading.Thread(target=adquisicionRFI, kwargs=kwargs_conf)
    hilo1.start()