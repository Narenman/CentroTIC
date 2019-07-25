import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json
import time
from sensado import Analogico

def suscriptor_MQTT():
    """Este es el suscriptor que se ejecuta en el esclavo
    para poder recibir las ordenes del maestro
    """
    def on_connect(client, userdata, flags, rc):
        client.subscribe("KITV2/Radiogis")
        if rc == 0:
            print("conexion exitosa con el broker")

    def on_message(client, userdata, message):
        msg = json.loads(message.payload.decode())

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"]=="aire":
            #API REST para enviar los datos cuando se reciban por MQTT
            lecturas = Analogico("192.168.0.103:8000")
            t1 = time.time()
            timming = 0
            while timming<=300:
                lecturas.calidadAire(msg["ubicacion"])
                timming = time.time()-t1
                time.sleep(1)
        
        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"]=="ph":
            #API REST para enviar los datos cuando se reciban por MQTT
            lecturas = Analogico("192.168.0.103:8000")
            t1 = time.time()
            timming = 0
            while timming<=300:
                lecturas.phAgua(msg["ubicacion"])
                timming = time.time()-t1
                time.sleep(1)

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"]=="turbidez":
            #API REST para enviar los datos cuando se reciban por MQTT
            lecturas = Analogico("192.168.0.103:8000")
            t1 = time.time()
            timming = 0
            while timming<=300:
                lecturas.turbidezAgua(msg["ubicacion"])
                timming = time.time()-t1
                time.sleep(1)
        
        client.disconnect()

    broker_address= "35.243.199.245"  
    port = 1883                  
    # broker_address= "centrotic1uis.cloudapp.net" 
    # port = 8443
    client = mqttClient.Client() 
    client.username_pw_set("pi", password="raspberry")    
    client.connect(broker_address, port=port)     
    client.on_connect= on_connect                 
    client.on_message= on_message                
    client.loop_forever()

if __name__ == "__main__":
    suscriptor_MQTT()