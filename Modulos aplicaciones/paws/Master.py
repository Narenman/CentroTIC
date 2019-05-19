import requests
import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json

def avail_spectrum_request(serial_Number, ruleset_Ids, model_Id, manufacturer_Id,dane_code,contact, email):
    """
    Este metodo se ejecuta en el maestro para preguntarle al servidor
    que espectro hay disponible para realizar una transmision
    AVAIL_SPECTRUM_REQ                                  
    +----------------------------------+-----------------+
    |deviceDesc:DeviceDescriptor       | see description |
    |location:GeoLocation              | see description |
    |owner:DeviceOwner                 | OPTIONAL        |
    |.................................|.................|
    """
    # serial_Number = "e310-f5ab-ao0x"
    # ruleset_Ids = "prototipo PAWS"
    # model_Id = "USRP E310"
    # manufacturer_Id = "Ettus Research"
    # dane_code = 68001
    # contact = "mario"
    # email = "luismiguel@radiogis.uis.edu.co"

    URL = "http://34.74.6.16/paws/avail-spectrum"
    AVAIL_SPECTRUM_REQ = {"serial_Number": serial_Number,
                            "ruleset_Ids": ruleset_Ids,
                            "model_Id": model_Id,
                            "manufacturer_Id": manufacturer_Id,
                            "dane_code": dane_code,
                            "contact": contact,
                            "email":email}

    r = requests.post(URL, data=AVAIL_SPECTRUM_REQ)
    if r.status_code==200:
        print("HTTP status ok. {}".format(r.status_code))
        AVAIL_SPECTRUM_RESP = r.text
        print(AVAIL_SPECTRUM_RESP)
        r.close()
        return AVAIL_SPECTRUM_RESP
    else:
        return None

def avail_spectrum_notify(serial_Number, ruleset_Ids, model_Id, manufacturer_Id,dane_code,spectra,operation):
    """
    Este metodo se ejecuta en el maestro para preguntarle al servidor
    que espectro hay disponible para realizar una transmision
    AVAIL_SPECTRUM_REQ                                  
    +----------------------------------+-----------------+
    |deviceDesc:DeviceDescriptor       | see description |
    |location:GeoLocation              | see description |
    |owner:DeviceOwner                 | OPTIONAL        |
    |.................................|.................|
    """
    # serial_Number = "e310-f5ab-ao0x"
    # ruleset_Ids = "prototipo PAWS"
    # model_Id = "USRP E310"
    # manufacturer_Id = "Ettus Research"
    # dane_code = 68001
    # contact = "mario"
    # email = "luismiguel@radiogis.uis.edu.co"

    URL = "http://127.0.0.1:8080/paws/spectrum-use-resp"
    SPECTRUM_USE_NOTIFY = {"serial_Number": serial_Number,
                            "ruleset_Ids": ruleset_Ids,
                            "model_Id": model_Id,
                            "manufacturer_Id": manufacturer_Id,
                            "dane_code": dane_code,
                            "spectra_use": spectra,
                            "operation": operation}

    r = requests.post(URL, data=SPECTRUM_USE_NOTIFY)
    if r.status_code==200:
        print("HTTP status ok. {}".format(r.status_code))
        AVAIL_SPECTRUM_RESP = r.text
        # print(AVAIL_SPECTRUM_RESP)
        r.close()
        return AVAIL_SPECTRUM_RESP
    else:
        return None

def suscriptor_MQTT_SPEC_RESP():
    """ suscriptor MQTT para el maestro, 
    esto es necesario debido a que la comunicacion con el esclavo
    es a traves del protocolo MQTT
    """
    def on_connect(client, userdata, flags, rc):
        client.subscribe("UIS/PAWS")
        if rc == 0:
            print("conexion exitosa con el broker")

    def on_message(client, userdata, message):
        # comunicacion entre el esclavo-maestro
        slave_msg = json.loads(message.payload.decode())
        serial_Number = slave_msg["serial_Number"]
        ruleset_Ids = slave_msg["ruleset_Ids"]
        model_Id = slave_msg["model_Id"]
        manufacturer_Id = slave_msg["manufacturer_Id"]
        dane_code = slave_msg["dane_code"]
        contact = slave_msg["contact"]
        email = slave_msg["email"]

        # comunicacion con entre el maestro-servidor
        AVAIL_SPECTRUM_RESP = avail_spectrum_request(serial_Number, ruleset_Ids, model_Id, manufacturer_Id,dane_code,contact, email)

        if AVAIL_SPECTRUM_RESP is not None:
            print(AVAIL_SPECTRUM_RESP)
            # aqui va el codigo para enviarle al esclavo sobre los canales libres
            publish.single("UIS/PAWS", AVAIL_SPECTRUM_RESP, port=1883, hostname=broker_address, auth={"username": usuario_broker, "password":password_broker})
        else:
            print("Comunicacion fallida con el servidor")
        client.disconnect()

    broker_address= "34.74.6.16"  
    port = 1883                  
    usuario_broker = "pi"
    password_broker = "raspberry"
    # broker_address= "centrotic1uis.cloudapp.net" 
    # port = 8443
    client = mqttClient.Client() # (a) crear un objeto
    client.username_pw_set(usuario_broker, password=password_broker)   
    client.connect(broker_address, port=port)    
    client.on_connect= on_connect                
    client.on_message= on_message                
    client.loop_forever() 


def suscriptor_MQTT_USE_NOTIFY():
    """ suscriptor MQTT del maestro para recibir la notificacion 
    de uso del espectro del esclavo
    """
    def on_connect(client, userdata, flags, rc):
        client.subscribe("UIS/PAWS")
        if rc == 0:
            print("conexion exitosa con el broker")

    def on_message(client, userdata, message):
        # comunicacion entre el esclavo-maestro
        slave_msg = json.loads(message.payload.decode())

        serial_Number = slave_msg["serial_Number"]
        ruleset_Ids = slave_msg["ruleset_Ids"]
        model_Id = slave_msg["model_Id"]
        manufacturer_Id = slave_msg["manufacturer_Id"]
        dane_code = slave_msg["dane_code"]
        spectra_use = slave_msg["spectra_use"]
        operation  = "dispositivo PAWS"
        print("canal escogido {}".format(spectra_use))
        print("notificacion recibida...\n{}".format(slave_msg))
        
        """ Comunicacion entre maestro-servidor para notificar el uso del espectro utilizado"""
        AVAIL_SPECTRUM_RESP = avail_spectrum_notify(serial_Number,ruleset_Ids,model_Id,manufacturer_Id,dane_code, spectra_use, operation)
        print(AVAIL_SPECTRUM_RESP)
        client.disconnect()

    broker_address= "34.74.6.16"  
    port = 1883                  
    usuario_broker = "pi"
    password_broker = "raspberry"
    # broker_address= "centrotic1uis.cloudapp.net" 
    # port = 8443
    client = mqttClient.Client() # (a) crear un objeto
    client.username_pw_set(usuario_broker, password=password_broker)   
    client.connect(broker_address, port=port)    
    client.on_connect= on_connect                
    client.on_message= on_message                
    client.loop_forever()

if __name__ == "__main__":
    suscriptor_MQTT_SPEC_RESP()
    suscriptor_MQTT_USE_NOTIFY()