from Monitoring import Monitoring
import requests
import time
import numpy
import json
import paho.mqtt.client as mqttClient


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

def monitoreo(frec_central, ganancia, samp_rate, tiempo, fft_size):
    """Entradas:
    * frec_central para indicar la frecuencia del VCO 78e6 <frec_central <5.92e9,
    * ganancia para indicar la ganacia del LNA 0<gain<70
    * samp_rate frecuencia de muestreo, solo toma valores discretos [32e3, 64e3, 125e3, 250e3, 500e3, 1e6,2e6,4e6,8e6,16e6]
    * tiempo es para indicar la duracion del sensado"""
    #objeto para realizar el sensado
    tb = Monitoring()
    tb.start()
    tb.set_freq(frec_central)
    tb.set_gain(ganancia)
    tb.set_samp_rate(samp_rate)
    tb.set_fft_size(fft_size)
    t1 = time.time()
    timming = 0
    while timming<=tiempo:
        timming = time.time()-t1
    tb.stop()
    tb.wait()
    print("fin del monitoreo...")

def envio_API(dispositivo, frec_central, samp_rate, fft_size):
    # objeto para leer el archivo del espectro
    x = numpy.fromfile('/home/root/centrotic/espectro', dtype=numpy.float32, count=-1)
    print("len(x)=", len(x))
    x = ComplexEncoder().encode(x)
    print("fin codificacion json")
    # envio por API REST
    pyload = {
        "espectro_IQ": x,
        "frec_central": frec_central,
        "dispositivo": dispositivo,
        "samp_rate": samp_rate,
        "fft_size": fft_size
    }

    headers={"Authorization": " Token 33565da4cc7e8394310dfa74160222e484b4fe6f"}
    # preparacion de las URL para realizar la actualizacion

    if frec_central==96e6 and dispositivo==1:
        URL = "http://192.168.0.105:8000/bloqueadores/espectro/1"
    elif frec_central==112e6 and dispositivo ==1:
        URL = "http://192.168.0.105:8000/bloqueadores/espectro/2"
    elif frec_central==96e6 and dispositivo ==2:
        URL = "http://192.168.0.105:8000/bloqueadores/espectro/3"
    elif frec_central==112e6 and dispositivo ==2:
        URL = "http://192.168.0.105:8000/bloqueadores/espectro/4"
    

    r = requests.put(URL, data=pyload, headers=headers)
    print("HTTP status {}".format(r.status_code))
    r.close()


class MQTTSuscriptor():
    def __init__(self, broker_address ="34.74.6.16",
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
        client.subscribe("USRP E310UIS LP 2131")

    def on_message(self, client, userdata, message):
            accion = message.payload.decode()
            accion = json.loads(accion)
            print(type(accion))
            print(accion)

            if accion["accion"] == "monitorear-espectro":
                """ Con esta instruccion el E310 sensa el espectro y envia los datos """
                #configuracion de variables
                fft_size = accion["fft_size"] # fft size,
                sample_rate = accion["sample_rate"]
                ganancia = accion["ganancia"]
                tiempo_sensado = accion["tiempo_sensado"] #segundos
                frecuencia_central = [96e6, 112e6]
                dispositivo = 1
                print(accion)
                #se inicia el proceso de escaneo
                for freq in frecuencia_central:
                    monitoreo(freq,ganancia,sample_rate,tiempo_sensado, fft_size)
                    envio_API(dispositivo, freq, sample_rate, fft_size)
                self.client.disconnect()

            if accion["accion"] == "bloquear-espectro":
                pass

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

