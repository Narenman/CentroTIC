from django.shortcuts import render
import paho.mqtt.publish as publish
from .forms import PozoForm
from django.contrib.auth.decorators import login_required
######
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import Temperatura, O2disuelto, PH, TemperaturaCaja, HumedadCaja, VoltajeBateria, TomaDatos
from django.http import HttpResponse
import time

# Create your views here.
def index(request):
    return render(request, "piscicultura/index.html", {})

@login_required
def registrar_pozo(request):
    pozo = PozoForm()
    if request.POST:
        pozo = PozoForm(request.POST)
        print(pozo.is_valid())
        if pozo.is_valid():
            pozo.save()
            return render(request, "piscicultura/index.html", {"registro": "registro exitoso del pozo"})
    else:
        respuesta = {"pozo": pozo}
    return render(request,"piscicultura/registrar_pozo.html",respuesta)

############################################################################

def monitoreo(request):
    return render(request,"piscicultura/monitoreo4.html",{})

@login_required
@csrf_exempt
def toma_datos(request):
    topico = "UIS/PISCICULTURA"
    IP_broker = "34.74.6.16"
    usuario_broker = "pi"
    password_broker = "raspberry"
    print("mqtt configurado")
    try:
        control = request.POST["info"]
        print("HI")
        #print(control)
        to_esp = {}
        if control == "activar":
            p = TomaDatos.objects.get(pk=1)
            p.estado = "Activado"
            p.save()
            """
            var_as = random.randint(1,100)
            asociacion = Asociacion(asociacion=var_as)
            asociacion.save()
            """
            to_esp.update({"control":control})
            to_esp = json.dumps(to_esp)
            print(to_esp)
            publish.single(topico, to_esp, port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})

        elif control == "desactivar":
            p = TomaDatos.objects.get(pk=1)
            p.estado = "Desactivado"
            p.save()

            to_esp.update({"control":control})
            to_esp = json.dumps(to_esp)
            print(to_esp)
            publish.single(topico, to_esp, port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})        
        
    except:
        pass
    return render(request, "piscicultura/toma_datos.html", {})
"""
def toma_datos(request):
    topico = "UIS/PISCICULTURA"
    IP_broker = "34.74.6.16"
    usuario_broker = "pi"
    password_broker = "raspberry"

    try:
        control = request.POST["info"]
        to_raspberry = {}    
    except:
        pass
    to_raspberry.update({"control": 1})
    to_raspberry = json.dumps(to_raspberry)
    publish.single(topico, to_raspberry, port=1883, hostname=IP_broker, auth={"username": usuario_broker, "password":password_broker})
    print(to_raspberry)
        
    return render(request, "piscicultura/toma_datos.html", {})
"""



@csrf_exempt
def last_json_data(request):

    temp = Temperatura.objects.last()
    #print(temp) 
    temperatura = [temp.fecha, temp.valor]
    #oxígeno disuelto
    od = O2disuelto.objects.last()
    oxigenoDisuelto = [od.fecha, od.valor]
    #ph
    ph = PH.objects.last()
    phTank = [ph.fecha, ph.valor]
    #temperatura caja
    tempC = TemperaturaCaja.objects.last()
    tempCaja = [tempC.fecha, tempC.valor]
    #voltaje batería
    bat=VoltajeBateria.objects.last()
    voltajeBat = [bat.fecha, bat.valor]
    #humedad caja
    humC = HumedadCaja.objects.last()
    humCaja = [humC.fecha, humC.valor]
    variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
    return JsonResponse(variables)


@csrf_exempt
def lecturas_json_all(request):
    #temperaturas
    temp = Temperatura.objects.all()
    temperatura = temp.values("fecha", "valor", "pozo")
    temperatura = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], temperatura))
    #oxígenodisuelto
    od = O2disuelto.objects.all()
    oxigenoDisuelto = od.values("fecha", "valor", "pozo")
    oxigenoDisuelto= list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], oxigenoDisuelto))
    #ph
    ph = PH.objects.all()
    phTank = ph.values("fecha", "valor", "pozo")
    phTank = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], phTank))
    #temperatura caja
    tempC = TemperaturaCaja.objects.all()
    tempCaja = tempC.values("fecha", "valor", "pozo")
    tempCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], tempCaja))
    #voltaje batería
    bat=VoltajeBateria.objects.all()
    voltajeBat = bat.values("fecha", "valor", "pozo")
    voltajeBat = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], voltajeBat))
    
    #humedad caja
    humC = HumedadCaja.objects.all()
    humCaja = humC.values("fecha","valor", "pozo")
    humCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], humCaja))
    
    variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
    return JsonResponse(variables)


@csrf_exempt
def json_estado(request):
    p = TomaDatos.objects.get(pk=1)
    respuesta={"estado": p.estado}
    print(respuesta)
    return JsonResponse(respuesta)