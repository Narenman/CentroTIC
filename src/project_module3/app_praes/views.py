from django.shortcuts import render
import paho.mqtt.publish as publish
from .models import Temperatura, Humedad, PresionAtmosferica, \
    Semillero, Integrantes, Kit, Asociacion
from .forms import IntegrantesForm, SemilleroForm, ConsultaSemilleroForm, ConsultaIntegrantesForm
from numpy import random
import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
import time

# Create your views here.

@login_required
@csrf_exempt
def control_ESP32(request):
    topico = "UIS/LP/213"
    IP_broker = "34.74.6.16"
    usuario_broker = "pi"
    password_broker = "raspberry"
    try:
        control = request.POST["info"]
        to_esp = {}
        if control == "modo-nariz":
            var_as = random.randint(1,100)
            asociacion = Asociacion(asociacion=var_as)
            asociacion.save()
            to_esp.update({"asociacion":asociacion.pk, "control":control})
            to_esp = json.dumps(to_esp)
            print(to_esp)
            publish.single(topico, to_esp, port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})

        else:
            to_esp.update({"asociacion":-20, "control":control})
            to_esp = json.dumps(to_esp)
            publish.single(topico, to_esp, port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})
            print(to_esp)
        
    except:
        pass
    return render(request, "app_praes/control_ESP32.html", {})

def index(request):
    respuesta = {}
    return render(request, "app_praes/index.html", respuesta)

def medicion_actual(request):
    respuesta = {}
    return render(request, "app_praes/medicion_actual.html", respuesta)

def monitoreo_lecturas(request):
    temp = Temperatura.objects.all()
    temperatura = temp.values("fecha", "valor")
    respuesta = {"temperatura": temperatura}
    return render(request, "app_praes/monitoreo_lecturas.html", respuesta)

@csrf_exempt
def monitoreo_lecturas_json(request):
    #temperaturas
    temp = Temperatura.objects.all()
    temperatura = temp.values("fecha", "valor")
    temperatura = list(map(lambda datos: [datos["fecha"], datos["valor"]], temperatura))
    #humedades
    hum = Humedad.objects.all()
    humedad = hum.values("fecha", "valor")
    humedad = list(map(lambda datos: [datos["fecha"], datos["valor"]], humedad))
    #presion
    pres = PresionAtmosferica.objects.all()
    presion = pres.values("fecha", "valor")
    presion = list(map(lambda datos: [datos["fecha"], datos["valor"]], presion))
   
    variables = {"temperatura":temperatura,
                  "humedad": humedad, "presion": presion,
                }
    return JsonResponse(variables)

def hora_local(request):
    """ para sincronizar la hora del servidor con la ESP32"""
    tz = timezone.now()
    resultado = {"GMT-5": tz}
    return JsonResponse(resultado)

@login_required
def registro_semillero(request):
    semillero = SemilleroForm()
    if request.POST:
        semillero = SemilleroForm(request.POST)
        if semillero.is_valid():
            semillero.save()
            return render(request, "app_praes/index.html", {"semillero": "Semillero registrado"})
    return render(request, "app_praes/registros_semillero.html", {"semillero": semillero})

@login_required
def registros_integrantes(request):
    integrantes = IntegrantesForm()
    if request.POST:
        integrantes = IntegrantesForm(request.POST)
        if integrantes.is_valid():
            integrantes.save()
            return render(request, "app_praes/index.html", {"integrantes": "Integrante registrado"})

    return render(request, "app_praes/registros_integrantes.html", {"integrantes": integrantes})

def consultar_semilleros(request):
    consulta_semillero = ConsultaSemilleroForm()
    try:
        dato = request.POST['colegio']
        semilleros = Semillero.objects.filter(colegio=dato)
        semilleros = semilleros.values("responsable", "telefono",)
        print(semilleros)

    except MultiValueDictKeyError:
        semilleros = []

    return render(request, "app_praes/consulta_semilleros.html", {"semillero": semilleros,
                                                                  "consulta": consulta_semillero})

def consultar_integrantes(request):
    consulta = ConsultaIntegrantesForm()
    print(request.POST)
    try:
        dato = request.POST['semillero']
        integrantes = Integrantes.objects.filter(semillero=dato)
        integrantes = integrantes.values("nombre", "telefono",)
        print(integrantes)
    except MultiValueDictKeyError:
        integrantes = []
    return render(request, "app_praes/consulta_integrantes.html", {"integrantes": integrantes,
                                                                   "consulta": consulta})

#Consulta de las variables ambientales individuales
@csrf_exempt
def consulta_temperatura(request):
    temperatura = Temperatura.objects.last()
    fecha = temperatura.fecha
    temperatura = temperatura.valor
    # temperatura = list(map(lambda datos: [datos["fecha"], datos["valor"]], temperatura))
    return JsonResponse({"temperatura": [temperatura, fecha]})

@csrf_exempt
def consulta_humedad(request):
    humedad = Humedad.objects.all()
    humedad = humedad.values("fecha", "valor")
    humedad = list(map(lambda datos: [datos["fecha"], datos["valor"]], humedad))
    return JsonResponse({"humedad": humedad})

@csrf_exempt
def consulta_presion(request):
    presion = PresionAtmosferica.objects.all()
    presion = presion.values("fecha", "valor")
    presion = list(map(lambda datos: [datos["fecha"], datos["valor"]], presion))
    return JsonResponse({"presion": presion})


def modo_nariz(request):
    """Esta vista se encarga pasar el dato recolectado por la nariz electronica v1 y evaluarlo con 
    el modelo entrenado para la nariz """

    #envio de informacion a la nariz para que inicie el escaneo de la muestra
    topico = "UIS/LP/213"
    IP_broker = "34.74.6.16"
    usuario_broker = "pi"
    password_broker = "raspberry"
    accion = {"control": "modo-nariz"}
    publish.single(topico, json.dumps(accion), port=1883, hostname=IP_broker,
    auth={"username": usuario_broker, "password":password_broker})

    #se necesita pausar el servidor mientras llegan nuevos datos a la base de datos
    time.sleep(6)
    
    return render(request,"app_praes/modo_nariz.html",{})
