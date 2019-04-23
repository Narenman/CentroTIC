import paho.mqtt.client as mqttClient
from DataTestSensor import *
import csv
import time
import threading
from Monitoreo import ThreadSensing
class MQTTSuscriptor():
    def __init__(self, broker_address ="34.73.25.149",
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
        self.hilo = ThreadSensing(False)

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("conexion exitosa con el broker")
        self.client.subscribe("UIS/NARIZ/PRINCIPAL")

    def on_message(self, client, userdata, message):
            accion = message.payload.decode()

            if accion == "adquirir-datos":
                """ Con esta instruccion la nariz comienza a recibir datos """
                self.hilo.escribir_csv()
                time.sleep(1)

            if accion == "control-electrovalvulas":
                pass

            if accion == "parar":
                """ Con esta instruccion la nariz desconecta la comunicacion con
                el broker """
                print(accion)
                global stop_thread
                stop_thread = True
                self.client.disconnect()
                print("se ha parado todo el proceso")

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 
        self.client.on_message= self.on_message              
        self.client.loop_forever()     
    
    def __del__(self):
        self.hilo.del_hilo()
        print("hilo fuera de base")


if __name__ == "__main__":
    while True:
        objmqtt = MQTTSuscriptor()
        objmqtt.comunicacionMQTT()
        del(objmqtt)