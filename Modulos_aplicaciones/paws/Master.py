import requests
import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json

def init_req(serial_Number, model_Id, manufacturer_Id,dane_code,):
    """ este metodo es para iniciar la comunicacion donde la base de datos
    retorna el init resp
    """
    URL = "http://35.243.199.245/paws/init-req"
    INIT_REQ = {"serial_Number": serial_Number,
                            "model_Id": model_Id,
                            "manufacturer_Id": manufacturer_Id,
                            "dane_code": dane_code}

    r = requests.post(URL, data=INIT_REQ)
    if r.status_code==200:
        print("HTTP status ok. {}".format(r.status_code))
        INIT_RESP = r.text
        INIT_RESP = json.loads(INIT_RESP)
        INIT_RESP = INIT_RESP["ruleset_info"]
        INIT_RESP =INIT_RESP[0]["rulsetId"]
        print(INIT_RESP)
        r.close()
        return INIT_RESP
    else:
        return None

def no_use_notify(serial_Number, ruleset_Ids, model_Id, manufacturer_Id,dane_code,chosen_channel):
    """ Este metodo es para eliminar los canales cuando el dispositivo en blanco deja de transmitir
    """
    URL = "http://35.243.199.245/paws/delete-channel-paws"
    AVAIL_SPECTRUM_REQ = {"serial_Number": serial_Number,
                            "ruleset_Ids": ruleset_Ids,
                            "model_Id": model_Id,
                            "manufacturer_Id": manufacturer_Id,
                            "dane_code": dane_code,
                            "freq_used": chosen_channel}

    r = requests.post(URL, data=AVAIL_SPECTRUM_REQ)
    if r.status_code==200:
        print("HTTP status ok. {}".format(r.status_code))
        AVAIL_SPECTRUM_RESP = r.text
        print(AVAIL_SPECTRUM_RESP)
        r.close()
        return AVAIL_SPECTRUM_RESP
    else:
        return None


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

    URL = "http://35.243.199.245/paws/avail-spectrum"
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
    Este metodo se ejecuta en el maestro para informarle al servidor el canal 
    que utilizara el esclavo para transmitir
    """
    # serial_Number = "e310-f5ab-ao0x"
    # ruleset_Ids = "prototipo PAWS"
    # model_Id = "USRP E310"
    # manufacturer_Id = "Ettus Research"
    # dane_code = 68001
    # contact = "mario"
    # email = "luismiguel@radiogis.uis.edu.co"

    URL = "http://35.243.199.245/paws/spectrum-use-resp"
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
            print("conexion exitosa con el broker\n spectrum resp")

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

    broker_address= "35.243.199.245"  
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
            print("conexion exitosa con el broker\nuse notify")

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
        
        """ Comunicacion entre maestro-servidor para notificar el uso del espectro utilizado"""
        AVAIL_SPECTRUM_RESP = avail_spectrum_notify(serial_Number,ruleset_Ids,model_Id,manufacturer_Id,dane_code, spectra_use, operation)
        print(AVAIL_SPECTRUM_RESP)
        client.disconnect()

    broker_address= "35.243.199.245"  
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


def suscriptor_MQTT_DELETE_NOTIFY():
    """ suscriptor MQTT del maestro para recibir la notificacion 
    de uso del espectro del esclavo
    """
    def on_connect(client, userdata, flags, rc):
        client.subscribe("UIS/PAWS")
        if rc == 0:
            print("conexion exitosa con el broker\ndelete notify")

    def on_message(client, userdata, message):
        # comunicacion entre el esclavo-maestro
        slave_msg = json.loads(message.payload.decode())

        serial_Number = slave_msg["serial_Number"]
        ruleset_Ids = slave_msg["ruleset_Ids"]
        model_Id = slave_msg["model_Id"]
        manufacturer_Id = slave_msg["manufacturer_Id"]
        dane_code = slave_msg["dane_code"]
        chosen_channel = slave_msg["freq_used"]
        
        """ Comunicacion entre maestro-servidor para notificar que ya no se 
        usara mas el canal notificado"""
        no_use_notify(serial_Number, ruleset_Ids, model_Id, manufacturer_Id,dane_code,chosen_channel)
        client.disconnect()

    broker_address= "35.243.199.245"  
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
    # informacion enviada para iniciar la comunicacion, deberia ser la info del 
    # en este caso el maestro tiene un esclavo.
    serial_Number = "e310-f5ab-ao0x"
    model_Id = "USRP E310"
    manufacturer_Id = "Ettus Research"
    dane_code = 68001

    # funciones principales del protoclo
    init_req(serial_Number, model_Id, manufacturer_Id, dane_code)
    suscriptor_MQTT_SPEC_RESP()
    suscriptor_MQTT_USE_NOTIFY()
    suscriptor_MQTT_DELETE_NOTIFY()