import paho.mqtt.client as mqttClient
from DataTestSensor import *
import csv
import time
import threading
import sys

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

            if accion == "adquirir-datos":
                """ Con esta instruccion la nariz comienza a recibir datos """
                print(accion)
                def imprime(num):
                    """ Hilo encargado de sensar los datos de la nariz y
                    almacenarlos en un archivo .csv"""
                    t = threading.currentThread()
                    try:
                        with open('employee_file'+str(num)+'.csv', mode='w') as employee_file:
                            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            while getattr(t, "do_run", True):
                                print("puta madre")
                                [fecha, valores] = dsensors()
                                employee_writer.writerow([fecha, valores])  
                    except:
                        pass

                t = threading.Thread(name="almacenar", target=imprime, args=(0, ))
                t.setDaemon(True)
                t.start()
                time.sleep(1)

            if accion == "control-electrovalvulas":
                pass

            if accion == "parar":
                """ Con esta instruccion la nariz desconecta la comunicacion con
                el broker """
                print(accion)
                t.do_run = False
                t.join()
                print("Sensado finalizado")
                client.disconnect()

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

if __name__ == "__main__":
    objmqtt = MQTTSuscriptor()
    objmqtt.comunicacionMQTT()