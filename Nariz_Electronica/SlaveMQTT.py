import paho.mqtt.client as mqttClient
from DataTestSensor import *

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
                [fecha, valores] = dsensors()

            if accion == "control-electrovalvulas":
                pass

            if accion == "parar":
                """ Con esta instruccion la nariz desconecta la comunicacion con
                el broker """
                client.disconnect()

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

if __name__ == "__main__":
    objmqtt = MQTTSuscriptor()
    objmqtt.comunicacionMQTT()