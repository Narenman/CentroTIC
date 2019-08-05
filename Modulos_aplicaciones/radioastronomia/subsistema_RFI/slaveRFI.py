import requests
import time
import numpy
import json
import paho.mqtt.client as mqttClient
from subsistemaRFI import subsistemaRFI
from Espectro import Espectro

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

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("conexion exitosa con el broker")
        client.subscribe("radioastronomia/RFI")

    def on_message(self, client, userdata, message):
            accion = message.payload.decode() #es el mensaje enviado por el cliente
            accion = json.loads(accion)

            if accion["accion"] == "modo manual":
                """ Con esta instruccion el E310 sensa el espectro y envia los datos """
                print(accion)
                #configuracion de variables
                fft_size = accion["nfft"] # fft size,
                sample_rate = accion["sample_rate"]
                ganancia = accion["ganancia"]
                tiempo_sensado = accion["duracion"] #segundos
                frec_central = accion["frec_central"]
                region = accion["region"]
                obj = Espectro(IP)
                #estado del sistema RFI
                activo = True
                obj.estado(activo)
                #control de los flujogramas
                obj.monitoreo(frec_central, ganancia, sample_rate, tiempo_sensado, fft_size)
                #envio del espectro y de las caracteristicas
                obj.envio_API(region, frec_central, sample_rate, fft_size, tiempo_sensado)
                #actualizacion del estado del sistema
                activo = False
                obj.estado(activo)
                self.client.disconnect()

            if accion["accion"] == "modo automatico":
                start_freq = accion["frecuencia_inicial"]
                stop_freq = accion["frecuencia_final"]
                samp_rate = accion["sample_rate"]
                tiempo_sensado = accion["duracion"]
                region = accion["region"]
                fft_size = accion["nfft"]
                ganancia = accion["ganancia"]

                #frecuencias para realizar el barrido del espectro
                frec_central = numpy.arange(start_freq, stop_freq, int(samp_rate/2))
                frec_central = frec_central[1:]
                
                #actualizacion del estado del sistema (ocupado=True)
                print(accion)

                obj = Espectro(IP)
                #inicio de adquisicion de datos
                for frec in frec_central:
                    print("frecuencia central: {}".format(frec))
                    obj.monitoreo(float(frec), ganancia, samp_rate, tiempo_sensado, fft_size)
                    obj.envio_API(region, float(frec), samp_rate, fft_size, tiempo_sensado)
                    activo = True
                    obj.estado(activo, frec)

                #actualizacion del estado del sistema
                activo = False
                obj.estado(activo, frec)

            # if accion["accion"] == "clasificacion-datos":
            #     pass

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

    def __del__(self):
        self.client.disconnect()


if __name__ == "__main__":
    global IP 
    IP = "192.168.0.103:8000"
    # IP = "10.1.50.216:8000" #dogulas

    while True:
        objmqtt = MQTTSuscriptor()
        objmqtt.comunicacionMQTT()
        del(objmqtt)
