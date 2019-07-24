import paho.mqtt.publish as publish
import json

#constantes
topico = "radioastronomia/RFI"
IP_broker = "34.74.6.16"
usuario_broker = "pi"
password_broker = "raspberry"

#variables de control RFI
nfft = 1024
sample_rate = 4000000 #S/s
ganancia = 50       #valor UHD
duracion = 1     #segundos
frec_central = 475000000
accion = True
region = 1      #paramo de berlin

#mensaje para MQTT
msg = {"nfft": nfft, "sample_rate": sample_rate, "ganancia": ganancia, "duracion": duracion, "frec_central": frec_central,
       "accion": accion, "region": region}

publish.single(topico, json.dumps(msg), port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})
