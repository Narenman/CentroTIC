import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json
import threading
from posicion import YaetsuG5500


def suscriptor_MQTT(**accion):
    """Este es el suscriptor que se ejecuta en el esclavo
    para poder recibir las ordenes del maestro
    """
    def on_connect(client, userdata, flags, rc):
        client.subscribe("radioastronomia/subsistemaposicion")
        if rc == 0:
            print("conexion exitosa con el broker")

    def on_message(client, userdata, message):
        msg = json.loads(message.payload.decode())
        print(msg)



#        if msg["modo"]=="manual":
#        azimut = msg["azimut"]
#        elevacion = msg["elevacion"]
#        region = msg["region"]
#        antena = msg["antena"]
#            controlador = YaetsuG5500()
#            controlador.control(azimut, elevacion, region, antena)
        
#        elif msg["modo"]=="automatico":

        azimut = msg["azimut"]
        elevacion = msg["elevacion"]
        region = msg["region"]
        antena = msg["antena"]
        controlador = YaetsuG5500(accion["IP_server"])
        controlador.control(int(azimut), int(elevacion), region, antena)


    broker_address= accion["IP_broker"]
    port = accion["PORT_broker"]
    # broker_address= "centrotic1uis.cloudapp.net
    # port = 8443
    client = mqttClient.Client()
    client.username_pw_set("pi", password="raspberry")
    client.connect(broker_address, port=port)
    client.on_connect= on_connect
    client.on_message= on_message
    client.loop_forever()


if __name__ == "__main__":
    global IP_server, IP_broker, PORT_broker
    IP_server = "192.168.0.113"
    IP_broker = "192.168.0.113"
    PORT_broker = 1883

    kwargs = {"IP_server": IP_server, "IP_broker":IP_broker, "PORT_broker": PORT_broker}
    hilo1 = threading.Thread(target=suscriptor_MQTT, kwargs=kwargs)
    hilo1.start()
