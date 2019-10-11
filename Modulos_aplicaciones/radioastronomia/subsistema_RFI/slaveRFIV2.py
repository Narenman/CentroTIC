import paho.mqtt.publish as publish
import threading
import paho.mqtt.client as mqttClient
import requests
import time
import numpy
import json
from subsistemaRFI import subsistemaRFI
from Espectro import Espectro

def manual(**accion):
    fft_size = accion["nfft"] # fft size,
    sample_rate = accion["sample_rate"]
    ganancia = accion["ganancia"]
    tiempo_sensado = accion["duracion"] #segundos
    frec_central = accion["frec_central"]
    region = accion["region"]
    #parametros del rotor
    azimut = accion["azimut"]
    elevacion = accion["elevacion"]
    antena = accion["antena"]
    topico = "radioastronomia/subsistemaposicion"

    #mensajes para controlador posicion
    msg = {"modo": "manual", "azimut": azimut,
            "elevacion": elevacion, "region": region,
            "antena": antena}
    MQTTSuscriptor().publishMQTT(topico, json.dumps(msg))

    #sistema RFI
    obj = Espectro(IP, usernameAPI, passwordAPI)
    #actualizacion de estados
    activo = True
    obj.estado(activo,frec_central, azimut, elevacion)
    obj.monitoreo(frec_central, ganancia, sample_rate, tiempo_sensado, fft_size) #control de los flujogramas
    obj.envio_API(region, frec_central, sample_rate, fft_size, tiempo_sensado, azimut, elevacion, antena)  #envio del espectro y de las caracteristicas
    #actualizacion del estado del sistema
    activo = False
    obj.estado(activo, frec_central, azimut, elevacion)

def automatico(**accion):
    topico = "radioastronomia/subsistemaposicion"
    start_freq = accion["frecuencia_inicial"]
    stop_freq = accion["frecuencia_final"]
    samp_rate = accion["sample_rate"]
    tiempo_sensado = accion["duracion"]
    region = accion["region"]
    fft_size = accion["nfft"]
    ganancia = accion["ganancia"]
    #parametros del rotor
    azinicial = accion["azinicial"]
    azfinal = accion["azfinal"]
    eleninicial = accion["eleninicial"]
    elefinal = accion["elefinal"]
    antena = accion["antena"]
    rbazimut = accion["RBazimut"]
    rbelevacion = accion["RBelevacion"]
    #configuracion de las resoluciones angulares y frecuenciales
    angazimut = numpy.arange(azinicial, azfinal, rbazimut)
    angelevacion = numpy.arange(eleninicial, elefinal, rbelevacion)
    frec_central = numpy.arange(start_freq, stop_freq, int(samp_rate))
    """El sistema realiza primero el barrido por frecuencias
    a un angulo de elevacion determinado, luego, el barrido
    por angulo azimut, sin embargo, cuando cambia al azimut
    se devuelve al ultimo elevacion, es para evitar 
    cambios bruscos en los angulos, por ejemplo: pasar de 90 a 0 grados
    en un instante """
    for az in angazimut:
        if stop_thread3==True:
            #actualizacion del estado del sistema
            obj = Espectro(IP, usernameAPI, passwordAPI)
            activo = False
            obj.estado(activo, 0, 1000, 1000)
            break
        else:
            pass
        #barrido para los angulos azimut
        for el in angelevacion:
            if stop_thread3==True:
                #actualizacion del estado del sistema
                obj = Espectro(IP, usernameAPI, passwordAPI)
                activo = False
                obj.estado(activo, 0, 1000, 1000)
                break
            else:
                pass
            #barrido para los angulos de elevacion y envio de controles al rotor
            #subsistema rotor
            msg = {"modo": "automatico", "azimut": az,
            "elevacion": el, "region": region,
            "antena": antena}
            MQTTSuscriptor().publishMQTT(topico, json.dumps(msg))
            #subsistema RFI
            obj = Espectro(IP, usernameAPI, passwordAPI)
            for frec in frec_central:
                if stop_thread3==True:
                    #actualizacion del estado del sistema
                    obj = Espectro(IP, usernameAPI, passwordAPI)
                    activo = False
                    obj.estado(activo, 0, 1000, 1000)
                    break
                else:
                    #barrido para las frecuencias
                    print("frecuencia central: {}".format(frec))
                    activo = True
                    obj.estado(activo, frec, az, el)
                    obj.monitoreo(float(frec), ganancia, samp_rate, tiempo_sensado, fft_size)
                    obj.envio_API(region, float(frec), samp_rate, fft_size, tiempo_sensado, az, el, antena)
        #para que la siguiente medida arranque en el ultimo angulo elevacion
        #y se devuelva
        angelevacion = numpy.flipud(angelevacion)
    #finalizacion de toma de datos
    activo = False
    obj.estado(activo, 0, 1000, 1000)

# funciones auxiliares
class MQTTSuscriptor():
    def __init__(self, broker_address ="35.243.199.245",
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

    def publishMQTT(self, topico, msg):
        """ Se encarga de establecer comunicacion
        MQTT con los dispositivos """
        publish.single(topico, msg, port=self.port, hostname=self.broker_address,
        auth={"username": self.usuario_broker, "password":self.contrasena_broker})

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("conexion exitosa con el broker")
        client.subscribe("radioastronomia/RFI")

    def on_message(self, client, userdata, message):
            accion = message.payload.decode() #es el mensaje enviado por el cliente
            accion = json.loads(accion)
            print(accion)
            global stop_thread2, stop_thread3
            stop_thread3 = False
            stop_thread2 = False

            if accion["accion"] == "modo manual":
                """ Con esta instruccion el E310 sensa el espectro y envia los datos """
                print(accion)
                #configuracion de variables provenientes del servidor
                fft_size = accion["nfft"] # fft size,
                sample_rate = accion["sample_rate"]
                ganancia = accion["ganancia"]
                tiempo_sensado = accion["duracion"] #segundos
                frec_central = accion["frec_central"]
                region = accion["region"]
                #parametros del rotor
                azimut = accion["azimut"]
                elevacion = accion["elevacion"]
                antena = accion["antena"]
                #mensajes para controlador posicion
                kwargs = {"nfft": fft_size, "sample_rate":sample_rate,
                "ganancia": ganancia, "duracion": tiempo_sensado, 
                "frec_central": frec_central, "region": region,
                "azimut": azimut, "elevacion": elevacion, "antena": antena}
                #hilo controlador
                hilo2 = threading.Thread(target=manual, kwargs=kwargs)
                hilo2.start()
                # self.client.disconnect()

            if accion["accion"] == "modo automatico":
                print(accion)
                start_freq = accion["frecuencia_inicial"]
                stop_freq = accion["frecuencia_final"]
                samp_rate = accion["sample_rate"]
                tiempo_sensado = accion["duracion"]
                region = accion["region"]
                fft_size = accion["nfft"]
                ganancia = accion["ganancia"]
                #parametros del rotor
                azinicial = accion["azinicial"]
                azfinal = accion["azfinal"]
                eleninicial = accion["eleninicial"]
                elefinal = accion["elefinal"]
                antena = accion["antena"]
                rbazimut = accion["RBazimut"]
                rbelevacion = accion["RBelevacion"]
                #hilo controlador
                kwargs = {"frecuencia_inicial": start_freq, "frecuencia_final":stop_freq,
                "sample_rate": samp_rate, "duracion": tiempo_sensado, "region": region, "nfft": fft_size,
                "ganancia": ganancia, "azinicial":azinicial, "azfinal":azfinal, "eleninicial": eleninicial,
                "elefinal": elefinal, "antena": antena, "RBazimut": rbazimut, "RBelevacion": rbelevacion}
                hilo3 = threading.Thread(target=automatico, kwargs=kwargs)
                hilo3.start()
                # self.client.disconnect()
            
            if accion["accion"] == "detener":
                stop_thread3 = True
                stop_thread2 = True

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

    def __del__(self):
        self.client.disconnect()


def adquisicionRFI(**conf):
    #aca iba un while
    objmqtt = MQTTSuscriptor(broker_address=conf["IP"], port=conf["port"], usuario_broker=conf["username"],
                            contrasena_broker=conf["password"])
    objmqtt.comunicacionMQTT()

if __name__ == "__main__":
    global IP, IPbroker, usernameAPI, passwordAPI
    global stop_thread2, stop_thread3
    stop_thread2 = False
    stop_thread3 = False

    # conexion servidor web
    IP = "35.243.199.245"
    usernameAPI  = "mario"
    passwordAPI = "mario"
    # conexion broker
    broker_address ="35.243.199.245"
    port = 1883
    usuario_broker = "pi"
    contrasena_broker = "raspberry"

    
    kwargs_conf = {"IP": broker_address, "port": port,
                   "username": usuario_broker, "password": contrasena_broker}
    hilo1 = threading.Thread(target=adquisicionRFI, kwargs=kwargs_conf)
    hilo1.start()
    
