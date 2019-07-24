from django.shortcuts import render
import paho.mqtt.publish as publish
from .models import Temperatura, Humedad, PresionAtmosferica, \
    Semillero, Integrantes, Kit, Asociacion, Sensores, PH_agua, Turbidez_agua, Temperatura_agua, Flujo_agua
from .forms import IntegrantesForm, SemilleroForm, ConsultaSemilleroForm, ConsultaIntegrantesForm, SensoresForm
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
    IP_broker = "35.243.199.245"
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

# aca van las vistas necesarias para mostrar las  variables ambientales
def medicion_actual_temperatura(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar temperatura")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/temperatura.html", respuesta)

@csrf_exempt
def consulta_temperatura(request):
    try:
        temperatura = Temperatura.objects.last()
        temperatura = [temperatura.fecha, temperatura.valor]
    except:
        fecha = timezone.now()
        temperatura = [fecha, 10]
    return JsonResponse({"temperatura": temperatura})

def medicion_actual_humedad(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar humedad")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/humedad.html", respuesta)

@csrf_exempt
def consulta_humedad(request):
    try:
        humedad = Humedad.objects.last()
        humedad = [humedad.fecha, humedad.valor]
    except:
        fecha = timezone.now()
        humedad = [fecha, 10]
    return JsonResponse({"temperatura": humedad})

def medicion_actual_presion(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar presion")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/presion.html", respuesta)

@csrf_exempt
def consulta_presion(request):
    try:
        presion = PresionAtmosferica.objects.last()
        presion = [presion.fecha, presion.valor]
    except:
        fecha = timezone.now()
        presion = [fecha, 100]
    return JsonResponse({"temperatura": presion})

def medicion_compuestos_aire(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar compuestos aire")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/compuestos_aire.html", respuesta)

def medicion_ph_agua(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar compuestos aire")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/ph_agua.html", respuesta)

@csrf_exempt
def consulta_ph(request):
    try:
        ph = PH_agua.objects.last()
        ph = [ph.fecha, ph.valor]
    except:
        fecha = timezone.now()
        ph = [fecha, 7]
    return JsonResponse({"temperatura": ph})

def medicion_turbidez(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar compuestos aire")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/turbidez.html", respuesta)

@csrf_exempt
def consulta_turbidez(request):
    try:
        turbidez = Turbidez_agua.objects.last()
        turbidez = [turbidez.fecha, turbidez.valor]
    except:
        fecha = timezone.now()
        turbidez = [fecha, 100]
    return JsonResponse({"temperatura": turbidez})


def medicion_temperatura_agua(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar compuestos aire")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/temperatura_agua.html", respuesta)

@csrf_exempt
def consulta_temp_agua(request):
    try:
        temp = Temperatura_agua.objects.last()
        temp = [temp.fecha, temp.valor]
    except:
        fecha = timezone.now()
        temp = [fecha, 16]
    return JsonResponse({"temperatura": temp})

def medicion_flujo_agua(request):
    """ Se encarga de la temperatura """
    sensores = SensoresForm()
    if request.POST:
        sensores = SensoresForm(request.POST)
        if sensores.is_valid():
            sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar compuestos aire")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/flujo_agua.html", respuesta)

@csrf_exempt
def consulta_flujo(request):
    try:
        temp = Flujo_agua.objects.last()
        temp = [temp.fecha, temp.valor]
    except:
        fecha = timezone.now()
        temp = [fecha, 800]
    return JsonResponse({"temperatura": temp})

def monitoreo_lecturas(request):
    """ Esta es la que debo modificar para cambiar la informacion """
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


def modo_nariz(request):
    """Esta vista se encarga pasar el dato recolectado por la nariz electronica v1 y evaluarlo con 
    el modelo entrenado para la nariz """

    #envio de informacion a la nariz para que inicie el escaneo de la muestra
    topico = "UIS/LP/213"
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    accion = {"control": "modo-nariz"}
    publish.single(topico, json.dumps(accion), port=1883, hostname=IP_broker,
    auth={"username": usuario_broker, "password":password_broker})

    #se necesita pausar el servidor mientras llegan nuevos datos a la base de datos
    time.sleep(6)
    
    return render(request,"app_praes/modo_nariz.html",{})
