import paho.mqtt.publish as publish
import threading
import paho.mqtt.client as mqttClient
import requests
import time
import random
import json
from Estacion import Estacion

def estadoestacion(estado):
    """esta funcion se encarga de actualizar el estado
    de la estacion metereologica """
    URL = "http://"+IP+"/radioastronomia/estado/estacion/1"
    data = {"estacion": estado}
    r = requests.put(URL, data=data)
    dato = r.text
    print("Estacion {}".format(dato))
    print("HTTP status code {} Actualizacion estado Estacion".format(r.status_code))
    r.close()

def consultaestados():
    URL = "http://"+IP+"/radioastronomia/estado/estacion/1"
    r = requests.get(url=URL)
    dato = r.text
    dato = json.loads(dato)
    return dato

def manual(**accion):
    """esta funcion se activa con el hilo de 
    adquisicion de datos manual desde la plataforma """
    region = accion["region"]
    estadoestacion(True)
    valores = {"temperatura": random.random(),
                "humedad_relativa": random.random(),
                "presion_atomosferica": random.random(),
                "radiacion_solar": random.random(),
                "vel_viento": random.random(),
                "dir_viento": "N-S",
                "precipitacion": random.random()}

    estacion = Estacion(IP, usernameAPI, passwordAPI)
    while True:
        estacion.estacionAPI(valores, region)
        if stop_thread2:
            estadoestacion(False)
            break

def automatico(**accion):
    """esta funcion se activa desde la adquisicion de modo automatico
    de la plataforma, sin embargo, es el mismo codigo que para modo manual pero
    para tener la misma filosofia de modos de operacion se deja asi. """
    region = accion["region"]
    estadoestacion(True)
    valores = {"temperatura": random.random(),
                "humedad_relativa": random.random(),
                "presion_atomosferica": random.random(),
                "radiacion_solar": random.random(),
                "vel_viento": random.random(),
                "dir_viento": "N-S",
                "precipitacion": random.random()}

    estacion = Estacion(IP, usernameAPI, passwordAPI)
    while True:
        estacion.estacionAPI(valores, region)
        if stop_thread3:
            estadoestacion(False)
            break
    

# funciones auxiliares
class MQTTSuscriptor():
    def __init__(self, broker_address ="35.243.199.245",
                       port = 1883,
                       usuario_broker = "pi",
                       contrasena_broker = "raspberry"):
        self.broker_address = broker_address
        self.port = port
        self.usuario_broker = usuario_broker
        self.contrasena_broker = contrasena_broker
        self.client = mqttClient.Client() 
        self.client.username_pw_set(self.usuario_broker, password=self.contrasena_broker) 
        self.client.connect(self.broker_address, port=self.port)    

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("conexion exitosa con el broker")
        client.subscribe("radioastronomia/RFI")

    def on_message(self, client, userdata, message):
        accion = message.payload.decode() #es el mensaje enviado por el cliente
        accion = json.loads(accion)
        print(accion)
        global stop_thread2, stop_thread3
        stop_thread3 = False
        stop_thread2 = False

        if accion["accion"] == "modo manual":
            region = accion["region"]
            kwargs = {"region": region}
            #aca hago la consulta del estado en la API
            estado = consultaestados()
            if estado["activo"]==False:
                #hilo controlador
                hilo2 = threading.Thread(target=manual, kwargs=kwargs)
                hilo2.start()
                # self.client.disconnect()
            else:
                print("El hilo de la estacion ya esta corriendo")

        if accion["accion"] == "modo automatico":
            region = accion["region"]
            kwargs = {"region": region}
            estado = consultaestados()
            if estado["activo"]==False:
                #aca hago la consulta del estado en la API              
                hilo3 = threading.Thread(target=automatico, kwargs=kwargs)
                hilo3.start()
                # self.client.disconnect()
            else:
                print("El hilo de la estacion ya esta corriendo")
        
        if accion["accion"] == "detener" or accion["accion"]=="detener-estacion":
            stop_thread3 = True
            stop_thread2 = True

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

    def __del__(self):
        self.client.disconnect()


def adquisicionestacion():
    #aca iba un while
    objmqtt = MQTTSuscriptor()
    objmqtt.comunicacionMQTT()

if __name__ == "__main__":
    global IP, IPbroker, usernameAPI, passwordAPI
    global stop_thread2, stop_thread3
    stop_thread2 = False
    stop_thread3 = False

    # IP = "192.168.0.101:8000"
    IP = "192.168.0.104:8000"
    IPbroker = "35.243.199.245"
    usernameAPI  = "mario"
    passwordAPI = "mario"
    hilo1 = threading.Thread(target=adquisicionestacion)
    hilo1.start()
    