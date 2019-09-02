"""Es para el subsistema RFI """
import requests
import numpy
import json
import time
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

class Espectro():
	"""Esta clase se encarga de leer el espectro, procesarlo para extraer 
	caracteristicas como el maximo, el minimo y la energia por cada vector almacenado,
	luego envia la informacion a las API que se encargan de redirigir la informacion
	hacia la base de datos """

	def __init__(self, IP, usernameAPI, passwordAPI):
		self.IP = IP
		self.usernameAPI = usernameAPI
		self.passwordAPI = passwordAPI

	def monitoreo(self, frec_central, ganancia, sample_rate, tiempo, nfft):
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


	def caracteristicas(self, x, nfft):
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
			# ener_ = 10*numpy.log10(ener_)
		return min_, max_, ener_

	#comunicacion con la API
	def getToken(self):
		"""Esta funcion se encarga de consultar el token de acuerdo al usuario
		y contrasena para la API """
		data = {
		"username": self.usernameAPI,
		"password": self.passwordAPI }
		URL = "http://"+self.IP+"/app_praes/token/"
		r = requests.post(URL, data=data)
		print("HTTP status token {}".format(r.status_code))
		token = json.loads(r.content)
		# print(token["token"])
		return token

	def consulta_id(self):
		url = "http://"+self.IP+"/radioastronomia/subsistema-RFI"
		
		token = self.getToken()		
		headers={"Authorization":"Token "+token["token"] }
		r = requests.get(url, headers=headers)
		dato = r.text
		dato = json.loads(dato)
		print(dato)
		print("HTTP status code {} consulta espectro".format(r.status_code))
		r.close()
		return dato["id"]

	def envio_API(self, region, frec_central, samp_rate, fft_size, duracion, azimut, elevacion, antena):
		# objeto para leer el archivo del espectro
		x = numpy.fromfile('/home/root/radioastronomia/espectro', dtype=numpy.float32, count=-1, sep='')
		print("len(x)=", len(x))
		min_v, max_v, energia = self.caracteristicas(x, fft_size)

		x = ComplexEncoder().encode(x)
		print("fin codificacion json")

		# envio por API REST
		pyload = { "espectro": x,
		"frec_muestreo": samp_rate,
		"nfft": fft_size,
		"frec_central": frec_central,
		"duracion": duracion,
		"region": region}
		token = self.getToken()
		headers={"Authorization": "Token "+token["token"]}
		# preparacion de las URL para realizar la actualizacion
		url = "http://"+self.IP+"/radioastronomia/subsistema-RFI"
		r = requests.post(url, data=pyload, headers=headers)
		print("HTTP status {} espectro".format(r.status_code))
		r.close()


		#actualizacion de la posicion
		pyload = {"azimut":azimut,
            "elevacion":elevacion,
            "region": region,
            "antena": antena}
		# preparacion de las URL para realizar la actualizacion
		url = "http://"+self.IP+"/radioastronomia/posicion-antena"
		r = requests.post(url, data=pyload, headers=headers)
		print("HTTP status {} posicion".format(r.status_code))
		r.close()

		#consulta id para actualizar las caracteristicas del espectro
		id = self.consulta_id()
		max_v = ComplexEncoder().encode(max_v)
		min_v = ComplexEncoder().encode(min_v)
		energia = ComplexEncoder().encode(energia)

		pyload = {
			"max_v": max_v,
			"min_v": min_v,
			"energia": energia,
			"espectro": id
			}
		url = "http://"+self.IP+"/radioastronomia/caracteristicas-espectro"
		r = requests.post(url, data=pyload, headers=headers)
		print("HTTP status {} caracteristicas espectro".format(r.status_code))
		r.close()

	def estado(self, activo, frecuencia, azimut, elevacion):
		"""Actualiza el estado de activo o inactivo, la entrada es:
		estado y es de tipo booleano """
		pyload = {"activo": activo,
				  "frecuencia": frecuencia,
				  "azimut": azimut,
				  "elevacion": elevacion}
		url = "http://"+self.IP+"/radioastronomia/estado/1"
		r = requests.put(url, pyload)
		print("HTTP {} actualizacion estado".format(r.status_code))
		r.close()

if __name__ == "__main__":
	IP = "127.0.0.1:8000"
	# usernameAPI = "mario"
	# passwordAPI = "mario"
	# obj_espectro = Espectro(IP, usernameAPI, passwordAPI)
	# obj_espectro.envio_API(1, 1000000, 32000, 1024, 20, 0,10,8)