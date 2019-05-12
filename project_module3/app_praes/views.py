from django.shortcuts import render
import paho.mqtt.publish as publish
from .models import Temperatura, Humedad, PresionAtmosferica, MaterialParticulado, NO2, \
    Polvo, O3, SO2, CO, CO2, MetanoPropanoCO, LuzUV, MaterialOrganico, CH4, Anemometro, \
    Semillero, Integrantes, Kit
from .forms import IntegrantesForm, SemilleroForm, ConsultaSemilleroForm, ConsultaIntegrantesForm

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
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
    temperatura = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], temperatura))
    #humedades
    hum = Humedad.objects.all()
    humedad = hum.values("fecha", "valor")
    humedad = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], humedad))
    #presion
    pres = PresionAtmosferica.objects.all()
    presion = pres.values("fecha", "valor")
    presion = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], presion))
    #sgp30 material organico, tambien lee CO2 pero ese lo leo con otro sensor
    voc = MaterialOrganico.objects.all()
    tvoc = voc.values("fecha", "valor")
    tvoc = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], tvoc))
    co2 = CO2.objects.all()
    CO2_ppm = co2.values("fecha", "valor")
    CO2_ppm = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], CO2_ppm))
    #ML8511 sensor UV
    uv = LuzUV.objects.all()
    luzuv = uv.values("fecha", "valor")
    luzuv = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], luzuv))

    #monoxido de carbono
    co=CO.objects.all()
    co = co.values("fecha", "valor")
    co = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], co))
    #metano CH4
    ch4 = CH4.objects.all()
    ch4 = ch4.values("fecha","valor")
    ch4 = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], ch4))
    #particulas de polvo
    polvo = Polvo.objects.all()
    polvo = polvo.values("fecha", "valor")
    polvo = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]],polvo))
    #so2 dioxido de azufre
    so2 = SO2.objects.all()
    so2 = so2.values("fecha", "valor")
    so2 = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]],so2))
    #no2 dioxido de nitrogeno
    no2 = NO2.objects.all()
    no2 = no2.values("fecha", "valor")
    no2 = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]],no2))
    #o3 ozono
    o3 = O3.objects.all()
    o3 = o3.values("fecha", "valor")
    o3 = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]],o3))
    #propano C3H8
    c3h8 = MetanoPropanoCO.objects.all()
    c3h8 = c3h8.values("fecha", "valor")
    c3h8 = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]],c3h8))


    variables = {"temperatura":temperatura,
                         "humedad": humedad, "presion": presion,
                         "tvoc": tvoc, "luzuv": luzuv, "co2": CO2_ppm,
                         "co":co, "ch4":ch4, "polvo":polvo, "so2":so2,
                         "no2":no2, "o3":o3, "c3h8":c3h8}
    return JsonResponse(variables)
@login_required
def control_ESP32(request):
    topico = "UIS/LP/213"
    IP_broker = "34.74.6.16"
    usuario_broker = "pi"
    password_broker = "raspberry"
    publish.single(topico, "ESP32-LED", port=1883, hostname=IP_broker,
    auth={"username": usuario_broker, "password":password_broker})
    respuesta = {}
    return render(request, "app_praes/control_ESP32.html", respuesta)

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
    temperatura = Temperatura.objects.all()
    temperatura = temperatura.values("fecha", "valor")
    temperatura = list(map(lambda datos: [datos["fecha"].timestamp(), datos["valor"]], temperatura))

    return JsonResponse({"temperatura": temperatura})