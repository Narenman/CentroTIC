import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json
import numpy
import time

def suscriptor_MQTT():
    """Este es el suscriptor que se ejecuta en el esclavo
    para poder recibir las ordenes del maestro
    """
    def on_connect(client, userdata, flags, rc):
        client.subscribe("UIS/PAWS")
        if rc == 0:
            print("conexion exitosa con el broker")

    def on_message(client, userdata, message):
        pass
        client.disconnect()

    broker_address= "34.74.6.16"  
    port = 1883                  
    # broker_address= "centrotic1uis.cloudapp.net" 
    # port = 8443
    client = mqttClient.Client() 
    client.username_pw_set("pi", password="raspberry")    
    client.connect(broker_address, port=port)     
    client.on_connect= on_connect                 
    client.on_message= on_message                
    client.loop_forever()