import paho.mqtt.publish as publish
import json

topico = "Primer KIT centrotic/1"
IP_broker = "35.243.199.245"
usuario_broker = "pi"
password_broker = "raspberry"
msg = json.dumps({"accion": "dato-en-vivo"})

publish.single(topico, msg, port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})