import json
import time
import paho.mqtt.publish as publish

from .models import Temperatura, Humedad, PresionAtmosferica, \
    Semillero, Integrantes, Kit, PH_agua, Turbidez_agua, Temperatura_agua, Flujo_agua, KitNariz
from .forms import IntegrantesForm, SemilleroForm, ConsultaSemilleroForm, ConsultaIntegrantesForm,\
    UbicacionForm

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def publishMQTT(topico, msg):
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    publish.single(topico, msg, port=1883, hostname=IP_broker,
     auth={"username": usuario_broker, "password":password_broker})

def index(request):
    respuesta = {}
    return render(request, "app_praes/index.html", respuesta)

# variables ambientales
def medicion_actual_temperatura(request):
    """ Se encarga de la temperatura """
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            print(request.POST)
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/temperatura.html", respuesta)

def medicion_actual_humedad(request):
    """ Se encarga de la temperatura """
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            # sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar humedad")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/humedad.html", respuesta)

def medicion_actual_presion(request):
    """ Se encarga de la temperatura """
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            # sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar presion")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/presion.html", respuesta)

#Aire
def medicion_compuestos_aire(request):
    """ Se encarga de la temperatura """
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            #validacion de datos para enviar instruccion MQTT
            dato = request.POST
            # print(dato)
            kit = Kit.objects.get(pk=dato["kit_monitoreo"])
            ubicacion = dato["ubicacion"]
            # datos para mqtt
            topico = kit.nombre_kit+"/"+str(kit.colegio)
            msg = json.dumps({"accion":"dato-en-vivo", "tipo dato":"aire",
                              "ubicacion": ubicacion})
            publishMQTT(topico,msg)
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/compuestos_aire.html", respuesta)

#Agua
def medicion_ph_agua(request):
    """ Se encarga de la temperatura """
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            #validacion de datos para enviar instruccion MQTT
            dato = request.POST
            # print(dato)
            kit = Kit.objects.get(pk=dato["kit_monitoreo"])
            ubicacion = dato["ubicacion"]
            # datos para mqtt
            topico = kit.nombre_kit+"/"+str(kit.colegio)
            msg = json.dumps({"accion":"dato-en-vivo", "tipo dato":"ph",
                              "ubicacion": ubicacion, "parar-aire": True})
            publishMQTT(topico,msg)
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/ph_agua.html", respuesta)

def medicion_turbidez(request):
    """ Se encarga de la temperatura """
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            #validacion de datos para enviar instruccion MQTT
            dato = request.POST
            # print(dato)
            kit = Kit.objects.get(pk=dato["kit_monitoreo"])
            ubicacion = dato["ubicacion"]
            # datos para mqtt
            topico = kit.nombre_kit+"/"+str(kit.colegio)
            msg = json.dumps({"accion":"dato-en-vivo", "tipo dato":"turbidez",
                              "ubicacion": ubicacion})
            publishMQTT(topico,msg)
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/turbidez.html", respuesta)

def medicion_temperatura_agua(request):
    """ Se encarga de la temperatura """
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            # sensores.save()
            ## enviar la orden MQTT para que se empieze a tomar la temperatura
            print(request.POST)
            print("tomar compuestos aire")
    respuesta = {"sensores": sensores}
    return render(request, "app_praes/temperatura_agua.html", respuesta)

#consulta de graficas
@csrf_exempt
def consulta_temperatura(request):
    try:
        temperatura = Temperatura.objects.last()
        temperatura = [temperatura.fecha, temperatura.valor]
    except:
        fecha = timezone.now()
        temperatura = [fecha, 10]
    return JsonResponse({"temperatura": temperatura})

@csrf_exempt
def consulta_humedad(request):
    try:
        humedad = Humedad.objects.last()
        humedad = [humedad.fecha, humedad.valor]
    except:
        fecha = timezone.now()
        humedad = [fecha, 10]
    return JsonResponse({"temperatura": humedad})

@csrf_exempt
def consulta_presion(request):
    try:
        presion = PresionAtmosferica.objects.last()
        presion = [presion.fecha, presion.valor]
    except:
        fecha = timezone.now()
        presion = [fecha, 100]
    return JsonResponse({"temperatura": presion})

@csrf_exempt
def consulta_compuestos_aire(request):
    try:
        nariz = KitNariz.objects.last()
        nariz = [nariz.fecha, nariz.valor]
    except:
        fecha = timezone.now()
        nariz = [fecha, [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10]]
    return JsonResponse({"temperatura": nariz})

@csrf_exempt
def consulta_ph(request):
    try:
        ph = PH_agua.objects.last()
        ph = [ph.fecha, ph.valor]
    except:
        fecha = timezone.now()
        ph = [fecha, 7]
    return JsonResponse({"temperatura": ph})

@csrf_exempt
def consulta_turbidez(request):
    try:
        turbidez = Turbidez_agua.objects.last()
        turbidez = [turbidez.fecha, turbidez.valor]
    except:
        fecha = timezone.now()
        turbidez = [fecha, 100]
    return JsonResponse({"temperatura": turbidez})

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
    sensores = UbicacionForm()
    if request.POST:
        sensores = UbicacionForm(request.POST)
        if sensores.is_valid():
            # sensores.save()
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
