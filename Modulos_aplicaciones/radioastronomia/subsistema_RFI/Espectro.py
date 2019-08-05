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

	def __init__(self, IP):
		self.IP = IP

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

	def consulta_id(self,):
		url = "http://"+self.IP+"/radioastronomia/subsistema-RFI"
		r = requests.get(url)
		dato = r.text
		dato = json.loads(dato)
		print(dato)
		print("HTTP status code {} consulta espectro".format(r.status_code))
		r.close()
		return dato["id"]

	def envio_API(self, region, frec_central, samp_rate, fft_size, duracion):
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
		# headers={"Authorization": "Token be9c008bdb9c0ed68f87863a1fdeda569a8fe4c7"}
		# preparacion de las URL para realizar la actualizacion
		url = "http://"+self.IP+"/radioastronomia/subsistema-RFI"
		r = requests.post(url, data=pyload)
		print("HTTP status {} espectro".format(r.status_code))
		r.close()

		#consulta id
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
		r = requests.post(url, data=pyload)
		print("HTTP status {} caracteristicas espectro".format(r.status_code))
		r.close()

	def estado(self, activo, frecuencia):
		"""Actualiza el estado de activo o inactivo, la entrada es:
		estado y es de tipo booleano """
		pyload = {"activo": activo,
				  "frecuencia": frecuencia}
		url = "http://"+self.IP+"/radioastronomia/estado/1"
		r = requests.put(url, pyload)
		print("HTTP {} actualizacion estado".format(r.status_code))
		r.close()

if __name__ == "__main__":
	IP = "127.0.0.1:8000"
	obj_espectro = Espectro(IP)
	obj_espectro.envio_API(1, 1000000, 32000, 1024, 20)