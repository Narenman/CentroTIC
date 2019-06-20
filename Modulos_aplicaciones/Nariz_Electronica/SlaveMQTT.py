import paho.mqtt.client as mqttClient
from DataTestSensor import *
import csv
import time
import threading
import sys
import json

import requests

class MQTTSuscriptor():
    def __init__(self, broker_address ="34.74.6.16",
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
                r = requests.post("http://34.74.6.16/nariz_electronica/lecturas", data=datos, headers={"Authorization":"Token be9c008bdb9c0ed68f87863a1fdeda569a8fe4c7"})
                print("HTTP status {}".format(r.status_code))
                r.close()

            if accion["accion"] == "control-electrovalvulas":
                pass

            if accion["accion"] == "clasificacion-datos":
                """ esta accion es para realizar el escaneo de la muestra para enviar al clasificador"""
                print("tomando datos ...")
                t1 = time.time()
                timeout = 0
                datos = []
                while timeout<=5:
                    [valores] = dsensors()
                    datos.append(valores)
                    t2 = time.time()
                    timeout = t2-t1
                print("fin toma de datos para clasificar")
                datos = {"medicion": json.dumps(datos)}
                url = "http://34.74.6.16/nariz_electronica/clasificar_datos"
                r = requests.post(url, data=datos)
                print("HTTP status {}".format(r.status_code))
                r.close()


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