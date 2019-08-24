import threading
import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json
import time
from sensado import AnalogicoDigital

def aire(**dato):
    lecturas = AnalogicoDigital(IPSERVER, APIusername, APIpassword)
    t1 = time.time()
    timming = 0
    while timming<=30:
        lecturas.calidadAire(dato["ubicacion"], dato["kit"])
        if stop_thread1:
            break
        print("aire")
        timming = time.time()-t1
        time.sleep(1)
    print("fin toma de datos")

def phagua(**dato):
    lecturas = AnalogicoDigital(IPSERVER, APIusername, APIpassword)
    t1 = time.time()
    timming = 0
    while timming<=30:
        lecturas.phAgua(dato["ubicacion"], dato["kit"])
        if stop_thread3:
            break
        print("ph agua")
        timming = time.time()-t1
        time.sleep(1)
    print("fin toma de datos")

def turbidez(**dato):
    lecturas = AnalogicoDigital(IPSERVER, APIusername, APIpassword)
    t1 = time.time()
    timming = 0
    while timming<=30:
        lecturas.turbidezAgua(dato["ubicacion"], dato["kit"])
        if stop_thread4:
            break
        print("turbidez agua")
        timming = time.time()- t1
        time.sleep(1)
    print("fin toma de datos")

def temperatura(**dato):
    lecturas = AnalogicoDigital(IPSERVER, APIusername, APIpassword)
    t1 = time.time()
    timming = 0
    while timming<=30:
        lecturas.climaTemperatura(dato["ubicacion"], dato["kit"])
        if stop_thread5:
            break
        print("temperatura")
        timming = time.time()- t1
        time.sleep(1)
    print("fin toma de datos")

def humedad(**dato):
    lecturas = AnalogicoDigital(IPSERVER, APIusername, APIpassword)
    t1 = time.time()
    timming = 0
    while timming<=30:
        lecturas.climaHumedad(dato["ubicacion"], dato["kit"])
        if stop_thread6:
            break
        print("humedad")
        timming = time.time()- t1
        time.sleep(1)
    print("fin toma de datos")

def presion(**dato):
    lecturas = AnalogicoDigital(IPSERVER, APIusername, APIpassword)
    t1 = time.time()
    timming = 0
    while timming<=30:
        lecturas.climaPresion(dato["ubicacion"], dato["kit"])
        if stop_thread7:
            break
        print("presion")
        timming = time.time()- t1
        time.sleep(1)
    print("fin toma de datos")

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
        kit = msg["kit"]
        global stop_thread1, stop_thread3, stop_thread4, stop_thread5, stop_thread6, stop_thread7

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"]=="aire":
            try:
                stop_thread1 = False # hilo de aire
                stop_thread3 = True  # hilo de ph
                stop_thread4 = True # hilo de turbidez
                stop_thread5 = True #hilo de temperatura
                stop_thread6  = True #hilo de humedad
                stop_thread7 = True #hilo de presion
                print("iniciando el hilo de aire")
                print("demas hilos finalizados")
                hilo1 = threading.Thread(target=aire, kwargs={"ubicacion":ubicacion, "kit":kit})
                hilo1.start()
            except:
                pass
        
        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"] =="ph":
            try:
                stop_thread3 = False # hilo de ph
                stop_thread4 = True  # hilo de turbidez
                stop_thread1 = True  # hilo de aire
                stop_thread5 = True #hilo de temperatura
                stop_thread6  = True #hilo de humedad
                stop_thread7 = True #hilo de presion
                print("hilos de aire, ph finalizados")
                print("iniciando hilo de ph")
                hilo3 = threading.Thread(target=phagua, kwargs={"ubicacion":ubicacion, "kit":kit})
                hilo3.start()
            except:
                pass
        
        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"] == "turbidez":
            try:
                stop_thread4 = False
                stop_thread1 = True
                stop_thread3 = True
                stop_thread5 = True # hilo de temperatura
                stop_thread6  = True # hilo de humedad
                stop_thread7 = True # hilo de presion
                print("hilo aire y ph finalizado")
                print("iniciando hilo de turbidez agua")
                hilo4 = threading.Thread(target=turbidez, kwargs={"ubicacion":ubicacion, "kit":kit})
                hilo4.start()
            except:
                pass

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"] == "temperatura":
            try:
                stop_thread5 = False # hilo de temperatura
                stop_thread1 = True
                stop_thread3 = True
                stop_thread4 = True
                stop_thread6  = True # hilo de humedad
                stop_thread7 = True # hilo de presion
                print("demas hilos finalizados")
                print("iniciando hilo de temperatura")
                hilo5 = threading.Thread(target=temperatura, kwargs={"ubicacion":ubicacion, "kit":kit})
                hilo5.start()
            except:
                pass

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"] == "humedad":
            try:
                stop_thread6  = False # hilo de humedad
                stop_thread1 = True
                stop_thread3 = True
                stop_thread4 = True
                stop_thread5 = True # hilo de temperatura
                stop_thread7 = True # hilo de presion
                print("demas hilos finalizados")
                print("iniciando hilo de humedad")
                hilo6 = threading.Thread(target=humedad, kwargs={"ubicacion":ubicacion, "kit":kit})
                hilo6.start()
            except:
                pass            

        if msg["accion"]=="dato-en-vivo" and msg["tipo dato"] == "presion":
            try:
                stop_thread7 = False # hilo de presion
                stop_thread1 = True
                stop_thread3 = True
                stop_thread4 = True
                stop_thread5 = True # hilo de temperatura
                stop_thread6  = True # hilo de humedad
                print("demas hilos finalizados")
                print("iniciando hilo de presion")
                hilo7 = threading.Thread(target=presion, kwargs={"ubicacion":ubicacion, "kit":kit})
                hilo7.start()
            except:
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
    #configuracion de variables
    global stop_thread1, stop_thread3, stop_thread4, stop_thread5, stop_thread6, stop_thread7
    global IPSERVER, APIusername, APIpassword
    IPSERVER = "192.168.0.103:8000"
    APIusername = "mario"
    APIpassword = "mario"
    stop_thread1 = False
    stop_thread3 = False
    stop_thread4 = False
    stop_thread5 = False
    stop_thread6 = False
    stop_thread7 = False
    #hilo maestro
    hilo2 = threading.Thread(target=suscriptor_MQTT)
    hilo2.start()