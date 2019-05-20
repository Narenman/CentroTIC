import paho.mqtt.client as mqttClient
from DataTestSensor import *
import csv
import time
import threading
import sys
import json

import requests

class MQTTSuscriptor():
    def __init__(self, broker_address ="34.73.25.149",
                       port = 1883,
                       usuario_broker = "pi",
                       contrasena_broker = "raspberry"):
        self.broker_address = broker_address
        self.port = port
        self.usuario_broker = usuario_broker
        self.contrasena_broker = contrasena_broker
        self.client = mqttClient.Client() # (a) crear un objeto
        self.client.username_pw_set(self.usuario_broker, password=self.contrasena_broker) # (b) configurar el usuario y contrasena
        self.client.connect(self.broker_address, port=self.port)     # (c) conexion con el broker 

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("conexion exitosa con el broker")
        client.subscribe("UIS/NARIZ/PRINCIPAL")

    def on_message(self, client, userdata, message):
            accion = message.payload.decode()
            accion = json.loads(accion)
            if accion["accion"] == "adquirir-datos":
                print(accion)
                """ Con esta instruccion la nariz comienza a recibir datos """
                t1 = time.time()
                timeout = 0
                datos = []
                """ sensado de la informacion"""

                while timeout<=accion["tiempo"]:
                    # [fecha, valores] = dsensors()
                    # datos.append([fecha, valores])
                    [valores] = dsensors()
                    datos.append(valores)
                    t2 = time.time()
                    timeout = t2-t1
                print("fin toma de datos")
                datos = { "medicion": json.dumps(datos),
                "analisis": accion["id"]}

                """ uso de la API """
                r = requests.post("http://34.73.25.149/nariz_electronica/lecturas", data=datos, headers={"Authorization":"Token be0f651e344c17b141e10f97f28b4a2fa0cdad7a"})
                print("HTTP status {}".format(r.status_code))
                r.close()

            if accion["accion"] == "control-electrovalvulas":
                pass


    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

    def __del__(self):
        self.client.disconnect()

if __name__ == "__main__":
    while True:
        objmqtt = MQTTSuscriptor()
        objmqtt.comunicacionMQTT()
        del(objmqtt)