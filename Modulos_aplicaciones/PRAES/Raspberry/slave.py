import threading
import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json
import time
from sensado import Analogico

def aire(**dato):
    lecturas = Analogico(IPSERVER)
    t1 = time.time()
    timming = 0
    while timming<=200:
        lecturas.calidadAire(dato["ubicacion"])
        if stop_thread1:
            break
        print("aire")
        timming = time.time()-t1
        time.sleep(1)

def phagua(**dato):
    lecturas = Analogico(IPSERVER)
    t1 = time.time()
    timming = 0
    while timming<=200:
        lecturas.phAgua(dato["ubicacion"])
        if stop_thread3:
            break
        print("ph agua")
        timming = time.time()-t1
        time.sleep(1)

def turbidez(**dato):
    lecturas = Analogico(IPSERVER)
    t1 = time.time()
    timming = 0
    while timming<=200:
        lecturas.turbidezAgua(dato["ubicacion"])
        if stop_thread4:
            break
        print("turbidez agua")
        timming = time.time()- t1
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
        ubicacion = msg["ubicacion"]

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"]=="aire":
            try:
                global stop_thread1, stop_thread3, stop_thread4
                stop_thread3 = True  # hilo de ph
                stop_thread4 = True # hilo de turbidez
                stop_thread1 = False # hilo de aire
                hilo3.join()
                hilo4.join()
                print("hilo agua finalizado")
            except:
                print("iniciando el hilo de aire")
                hilo1 = threading.Thread(target=aire, kwargs={"ubicacion":ubicacion})
                hilo1.start()
                pass
        
        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"] =="ph":
            try:
                global stop_thread1, stop_thread3, stop_thread4
                stop_thread4 = True  # hilo de turbidez
                stop_thread1 = True  # hilo de aire
                stop_thread3 = False # hilo de ph
                hilo1.join()
                hilo4.join()
                print("hilos de aire, ph finalizados")
            except:
                print("iniciando hilo de ph")
                hilo3 = threading.Thread(target=phagua, kwargs={"ubicacion":ubicacion})
                hilo3.start()
                pass
        
        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"] == "turbidez":
            try:
                global stop_thread1, stop_thread3, stop_thread4
                stop_thread1 = True
                stop_thread3 = True
                stop_thread4 = False
                hilo1.join()
                hilo3.join()
                print("hilo aire y ph finalizado")
            except:
                print("iniciando hilo de turbidez agua")
                hilo4 = threading.Thread(target=turbidez, kwargs={"ubicacion":ubicacion})
                hilo4.start()
                pass
            

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
    global stop_thread1, stop_thread3, stop_thread4
    global IPSERVER
    IPSERVER = "192.168.0.103:8000"
    stop_thread1 = False
    stop_thread3 = False
    stop_thread4 = False
    hilo2 = threading.Thread(target=suscriptor_MQTT)
    hilo2.start()