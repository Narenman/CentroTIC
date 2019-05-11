from django.shortcuts import render
import paho.mqtt.client as mqttClient

# Create your views here.
def index(request):
    return render(request, "nariz_electronicaV2/index.html", {})

def control_narizV2(request):

    """ Esta seccion de codigo realiza una publicacion
    a la E-NOSE"""
    def on_connect(client, userdata, flags, rc):
        client.subscribe("UIS/E-NOSE/v15")
        if rc == 0:
            print("Conexion con el broker")
        else:
            print("Conexion fallida")

    #VM google cloud
    broker_address= "34.74.6.16" 
    port = 1883

    #VM Azure 
    # broker_address= "centrotic1uis.cloudapp.net" 
    # port = 8443

    client = mqttClient.Client()     
    client.username_pw_set("pi", password="raspberry")   
    client.connect(broker_address, port=port)          
    client.publish("UIS/E-NOSE/v15", "ESP32-LED")       
    client.disconnect()                               
    #########################################

    

    return render(request, "nariz_electronicaV2/control_narizV2.html", {})