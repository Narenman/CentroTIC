import threading

import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json
import time
from sensado import Analogico

def contar(**dato):
    lecturas = Analogico("192.168.0.103:8000")
    t1 = time.time()
    timming = 0
    while timming<=300:
        lecturas.calidadAire(dato["ubicacion"])
        print("aire")
        timming = time.time()-t1
        time.sleep(1)

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
        print(msg)

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"]=="aire":
            hilo1.start()
            pass

        if msg["parar-aire"]==True:
            print("puta madre")
            hilo1.join()
            client.disconnect()
        # client.disconnect()

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
    hilo2 = threading.Thread(target=suscriptor_MQTT)
    hilo1 = threading.Thread(target=contar, kwargs={"ubicacion":1})
    # hilo1.start()
    hilo2.start()









