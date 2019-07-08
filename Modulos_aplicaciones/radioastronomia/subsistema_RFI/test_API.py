"""Es para el subsistema RFI """
import requests
import numpy
import json


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


x = numpy.fromfile('/home/uis-e3t/back_centrotic/CentroTIC/Modulos_aplicaciones/radioastronomia/subsistema RFI/espectro', dtype=numpy.float32, count=-1)
x = ComplexEncoder().encode(x[0:4096])

pyload = { "espectro": x,
  "frec_muestreo": 16000000,
  "nfft": 4096,
  "frec_central": 50000000,
  "duracion": 20,
  "region": 1
}


url = "http://127.0.0.1:8000/radioastronomia/subsistema-RFI"

r = requests.post(url, data=pyload)
print(r.status_code)
r.close()