import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
import json
import numpy
import time

from TVWS import TVWS
import time

def transmision(freq, event_time):
    tb = TVWS()
    tb.start()
    freq = freq*1e6
    print(freq, "frecuencia escogida para transmitir")
    tb.set_freq(freq)
    t1 = time.time()
    timming = 0

    while timming<=event_time:
        timming = time.time()-t1

    tb.stop()
    tb.wait()

def avail_spectrum_request():
    """Este metodo se ejecuta en el esclavo-SDR para preguntarle al maestro
    y que este haga la consulta al servidor
    """
    # informacion dispositivo esclavo
    serial_Number = "e310-f5ab-ao0x"
    ruleset_Ids = "prototipo PAWS"
    model_Id = "USRP E310"
    manufacturer_Id = "Ettus Research"
    dane_code = 68001 # codigo dane para Bucaramanga
    contact = "mario"
    email = "luismiguel@radiogis.uis.edu.co"

    # informacion Broker MQTT
    topico = "UIS/PAWS"
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"

    AVAIL_SPECTRUM_REQ = {"serial_Number": serial_Number,
                        "ruleset_Ids": ruleset_Ids,
                        "model_Id": model_Id,
                        "manufacturer_Id": manufacturer_Id,
                        "dane_code": dane_code,
                        "contact": contact,
                        "email":email}
                        
    publish.single(topico, json.dumps(AVAIL_SPECTRUM_REQ), port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})
    return None

def spectrum_use_notify(spectra):
    """+---------------------------------------------------+
    |SPECTRUM_USE_NOTIFY                                |
    +---------------------------------+-----------------+
    |deviceDesc:DeviceDescriptor      | REQUIRED        |
    |location:GeoLocation             | see description |
    |spectra:list                     | REQUIRED        |"""
    # informacion dispositivo esclavo
    serial_Number = "e310-f5ab-ao0x"
    ruleset_Ids = "prototipo PAWS"
    model_Id = "USRP E310"
    manufacturer_Id = "Ettus Research"
    dane_code = 68001 # codigo dane para Bucaramanga
    #informacion del broker
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"

    SPECTRUM_USE_NOTIFY = {"serial_Number":serial_Number,
                        "model_Id":model_Id,
                        "ruleset_Ids":ruleset_Ids,
                        "manufacturer_Id": manufacturer_Id,
                        "dane_code": dane_code,
                        "spectra_use":spectra}

    publish.single("UIS/PAWS", json.dumps(SPECTRUM_USE_NOTIFY), port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})


def suscriptor_MQTT():
    """Este es el suscriptor que se ejecuta en el esclavo
    para poder recibir las ordenes del maestro
    """
    def on_connect(client, userdata, flags, rc):
        client.subscribe("UIS/PAWS")
        if rc == 0:
            print("conexion exitosa con el broker")

    def on_message(client, userdata, message):
        global chosen_channel
        master_msg = json.loads(message.payload.decode()) # mensaje recibido por el maestro

        free_spectra = master_msg["free_spectra"] # lista de los canales libres para transmision
        rand_index = numpy.random.randint(len(free_spectra)) # seleccion aleatoria del canal escogido
        chosen_channel = free_spectra[rand_index]    # canal escogido por el esclavo

        spectrum_use_notify(chosen_channel) #envio al maestro del canal escogido
        client.disconnect()

    broker_address= "35.243.199.245"  
    port = 1883                  
    # broker_address= "centrotic1uis.cloudapp.net" 
    # port = 8443
    client = mqttClient.Client() 
    client.username_pw_set("pi", password="raspberry")    
    client.connect(broker_address, port=port)     
    client.on_connect= on_connect                 
    client.on_message= on_message                
    client.loop_forever()

if __name__ == "__main__":
    global chosen_channel
    avail_spectrum_request() # solicitud al maestro del espectro disponible
    suscriptor_MQTT()
    """ el esclavo se queda transmitiendo durante un tiempo """
    event_time = 45
    print("transmitiendo ....")
    transmision(chosen_channel,event_time)
    # cuando termina de transmitir debe notificar al maestro que 
    # ya no esta usando esa frecuencia para borrarla de la base de datos
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    SPECTRUM_DELETE_NOTIFY = { "serial_Number": "e310-f5ab-ao0x",
                                "ruleset_Ids": "prototipo PAWS",
                                "model_Id": "USRP E310",
                                "manufacturer_Id": "Ettus Research",
                                "dane_code": 68001,
                                "freq_used": chosen_channel,}
    publish.single("UIS/PAWS", json.dumps(SPECTRUM_DELETE_NOTIFY), port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})
    print("fin transmision ...")
