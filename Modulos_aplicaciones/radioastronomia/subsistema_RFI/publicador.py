import paho.mqtt.publish as publish
import json

#constantes
topico = "radioastronomia/RFI"
IP_broker = "35.243.199.245"
usuario_broker = "pi"
password_broker = "raspberry"

#variables de control RFI
nfft = 1024
sample_rate = 4000000 #S/s
frec_central = 475000000
ganancia = 50       #valor UHD
duracion = 1     #segundos
accion = True
region = 1      #paramo de berlin

#mensaje para MQTT
msg = {"nfft": nfft, "sample_rate": sample_rate, "ganancia": ganancia, "duracion": duracion, "frec_central": frec_central,
       "accion": accion, "region": region}

publish.single(topico, json.dumps(msg), port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})



