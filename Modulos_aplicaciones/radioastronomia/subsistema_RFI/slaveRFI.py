import requests
import time
import numpy
import json
import paho.mqtt.client as mqttClient
from subsistemaRFI import subsistemaRFI

class ComplexEncoder(json.JSONEncoder):
	""" Para codificar las muestras complejas en json"""
	def default(self, obj):
		if isinstance(obj, (numpy.ndarray,numpy.number)):
			return obj.tolist()
		elif isinstance(obj, (complex, numpy.complex)):
			return [obj.real, obj.imag]
		elif isinstance(obj, set):
			return list(obj)
		elif isinstance(obj, bytes):  # pragma: py3
			return obj.decode()
		return json.JSONEncoder.default(self, obj)


def monitoreo(frec_central, ganancia, sample_rate, tiempo, nfft):
    """Entradas:
    * frec_central para indicar la frecuencia del VCO 78e6 <frec_central <5.92e9,
    * ganancia para indicar la ganacia del LNA 0<gain<70
    * samp_rate frecuencia de muestreo, solo toma valores discretos [32e3, 64e3, 125e3, 250e3, 500e3, 1e6,2e6,4e6,8e6,16e6]
    * tiempo es para indicar la duracion del sensado"""
    #objeto para realizar el sensado
    tb = subsistemaRFI()
    tb.start()
    tb.set_frec_central(frec_central)
    tb.set_ganancia(ganancia)
    tb.set_samp_rate(sample_rate)
    tb.set_nfft(nfft)
    t1 = time.time()
    timming = 0
    while timming<=tiempo:
        timming = time.time()-t1
    tb.stop()
    tb.wait()
    print("fin del monitoreo...")

def caracteristicas(x, nfft):
    """ Esta funcion extrae caracteristicas basicas
    del espectro sensado"""
    frames = int(len(x)/nfft)
    min_ = numpy.array([])
    max_ = numpy.array([])
    ener_ = numpy.array([])
    for i in range(frames-1):
        min_= numpy.append(min_, numpy.min(x[i*nfft:nfft*(i+1)]))
        max_= numpy.append(max_, numpy.max(x[i*nfft:nfft*(i+1)]))
        ener_ = numpy.append(ener_, numpy.sum(10**((x[nfft*i:nfft*(i+1)])/10.0)))
        ener_ = 10*numpy.log10(ener_)
    return min_, max_, ener_

def envio_API(region, frec_central, samp_rate, fft_size, duracion):
    # objeto para leer el archivo del espectro
    x = numpy.fromfile('/home/root/radioastronomia/espectro', dtype=numpy.float32, count=-1)
    print("len(x)=", len(x))
    x = ComplexEncoder().encode(x)
    print("fin codificacion json")

    # envio por API REST
    pyload = { "espectro": x,
    "frec_muestreo": samp_rate,
    "nfft": fft_size,
    "frec_central": frec_central,
    "duracion": duracion,
    "region": region}

    # headers={"Authorization": " Token be9c008bdb9c0ed68f87863a1fdeda569a8fe4c7"}
    # preparacion de las URL para realizar la actualizacion
    url = "http://192.168.0.103:8000/radioastronomia/subsistema-RFI"

    r = requests.post(url, data=pyload)
    print("HTTP status {}".format(r.status_code))
    r.close()


class MQTTSuscriptor():
    def __init__(self, broker_address ="35.243.199.245",
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
        client.subscribe("radioastronomia/RFI")

    def on_message(self, client, userdata, message):
            accion = message.payload.decode()
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
                #aca coloco el codigo para controlar los flujogramas
                monitoreo(frec_central, ganancia, sample_rate, tiempo_sensado, fft_size)
                envio_API(region, frec_central, sample_rate, fft_size, tiempo_sensado)

                self.client.disconnect()

            if accion["accion"] == "modo automatico":
                start_freq = accion["frecuencia_inicial"]
                stop_freq = accion["frecuencia_final"]
                samp_rate = accion["sample_rate"]
                tiempo_sensado = accion["duracion"]
                region = accion["region"]
                fft_size = accion["nfft"]
                ganancia = accion["ganancia"]

                frec_central = numpy.arange(start_freq, stop_freq, int(samp_rate/2))
                frec_central = frec_central[1:]
                
                print(type(frec_central[0]))
                print(accion)
                for frec in frec_central:
                    print("frecuencia central: {}".format(frec))
                    monitoreo(float(frec), ganancia, samp_rate, tiempo_sensado, fft_size)
                    envio_API(region, float(frec), samp_rate, fft_size, tiempo_sensado)

            # if accion["accion"] == "clasificacion-datos":
            #     pass

    def comunicacionMQTT(self):
        self.client.on_connect= self.on_connect                 # (d) suscriptor
        self.client.on_message= self.on_message                 # (d) suscriptor
        self.client.loop_forever()                              # (e) mantener conexion con el broker

    def __del__(self):
        self.client.disconnect()


if __name__ == "__main__":
    while True:
        objmqtt = MQTTSuscriptor()
        objmqtt.comunicacionMQTT()
        del(objmqtt)
