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
    IP_broker = "192.168.1.5"
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

def json_last_est1(request):
    temp = Temperatura.objects.filter(pozo_id=1)
    #print(temp)
    temp = temp.last()
    #print(temp) 
    temperatura = [temp.fecha, temp.valor]
    #oxígeno disuelto
    od = O2disuelto.objects.filter(pozo_id=1)
    od = od.last()
    oxigenoDisuelto = [od.fecha, od.valor]
    #ph
    ph = PH.objects.filter(pozo_id=1)
    ph = ph.last()
    phTank = [ph.fecha, ph.valor]
    #temperatura caja
    tempC = TemperaturaCaja.objects.filter(pozo_id=1)
    tempC = tempC.last()
    tempCaja = [tempC.fecha, tempC.valor]
    #voltaje batería
    bat=VoltajeBateria.objects.filter(pozo_id=1)
    bat = bat.last()
    voltajeBat = [bat.fecha, bat.valor]
    #humedad caja
    humC = HumedadCaja.objects.filter(pozo_id=1)
    humC = humC.last()
    humCaja = [humC.fecha, humC.valor]
    variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
    # print(variables)
    return JsonResponse(variables)

@csrf_exempt
def json_last_est2(request):
    try:
        temp = Temperatura.objects.filter(pozo_id=2)
        #print(temp)
        temp = temp.last()
        #print(temp) 
        temperatura = [temp.fecha, temp.valor]
        #oxígeno disuelto
        od = O2disuelto.objects.filter(pozo_id=2)
        od = od.last()
        oxigenoDisuelto = [od.fecha, od.valor]
        #ph
        ph = PH.objects.filter(pozo_id=2)
        ph = ph.last()
        phTank = [ph.fecha, ph.valor]
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=2)
        tempC = tempC.last()
        tempCaja = [tempC.fecha, tempC.valor]
        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=2)
        bat = bat.last()
        voltajeBat = [bat.fecha, bat.valor]
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=2)
        humC = humC.last()
        humCaja = [humC.fecha, humC.valor]
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
        # print(variables)
    except:
        variables = {}
    return JsonResponse(variables)

def json_last_est3(request):
    try:
        temp = Temperatura.objects.filter(pozo_id=3)
        #print(temp)
        temp = temp.last()
        #print(temp) 
        temperatura = [temp.fecha, temp.valor]
        #oxígeno disuelto
        od = O2disuelto.objects.filter(pozo_id=3)
        od = od.last()
        oxigenoDisuelto = [od.fecha, od.valor]
        #ph
        ph = PH.objects.filter(pozo_id=3)
        ph = ph.last()
        phTank = [ph.fecha, ph.valor]
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=3)
        tempC = tempC.last()
        tempCaja = [tempC.fecha, tempC.valor]
        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=3)
        bat = bat.last()
        voltajeBat = [bat.fecha, bat.valor]
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=3)
        humC = humC.last()
        humCaja = [humC.fecha, humC.valor]
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
        # print(variables)
    except:
        variables = {}
    return JsonResponse(variables)

@csrf_exempt
def json_all_est1(request):
    try:
        #temperaturas
        temp = Temperatura.objects.filter(pozo_id=1)
        #print(temp)
        temperatura = temp.values("fecha", "valor", "pozo")
        #print(temperatura) 
        temperatura = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], temperatura))
        #oxígenodisuelto
        od = O2disuelto.objects.filter(pozo_id=1)
        oxigenoDisuelto = od.values("fecha", "valor", "pozo")
        oxigenoDisuelto= list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], oxigenoDisuelto))
        #ph
        ph = PH.objects.filter(pozo_id=1)
        phTank = ph.values("fecha", "valor", "pozo")
        phTank = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], phTank))
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=1)
        tempCaja = tempC.values("fecha", "valor", "pozo")
        tempCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], tempCaja))
        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=1)
        voltajeBat = bat.values("fecha", "valor", "pozo")
        voltajeBat = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], voltajeBat))
        
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=1)
        humCaja = humC.values("fecha","valor", "pozo")
        humCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], humCaja))
        
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
    except:
        variables = {}

    return JsonResponse(variables)

@csrf_exempt
def json_all_est2(request):
    try:
        #temperaturas
        temp = Temperatura.objects.filter(pozo_id=2)
        temperatura = temp.values("fecha", "valor", "pozo")
        temperatura = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], temperatura))
        #oxígenodisuelto
        od = O2disuelto.objects.filter(pozo_id=2)
        oxigenoDisuelto = od.values("fecha", "valor", "pozo")
        oxigenoDisuelto= list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], oxigenoDisuelto))
        #ph
        ph = PH.objects.filter(pozo_id=2)
        phTank = ph.values("fecha", "valor", "pozo")
        phTank = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], phTank))
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=2)
        tempCaja = tempC.values("fecha", "valor", "pozo")
        tempCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], tempCaja))
        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=2)
        voltajeBat = bat.values("fecha", "valor", "pozo")
        voltajeBat = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], voltajeBat)) 
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=2)
        humCaja = humC.values("fecha","valor", "pozo")
        humCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], humCaja))
        
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
    except:
        variables = {}

    return JsonResponse(variables)

@csrf_exempt
def json_all_est3(request):
    try:
        #temperaturas
        temp = Temperatura.objects.filter(pozo_id=3)
        temperatura = temp.values("fecha", "valor", "pozo")
        temperatura = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], temperatura))
        #oxígenodisuelto
        od = O2disuelto.objects.filter(pozo_id=3)
        oxigenoDisuelto = od.values("fecha", "valor", "pozo")
        oxigenoDisuelto= list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], oxigenoDisuelto))
        #ph
        ph = PH.objects.filter(pozo_id=3)
        phTank = ph.values("fecha", "valor", "pozo")
        phTank = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], phTank))
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=3)
        tempCaja = tempC.values("fecha", "valor", "pozo")
        tempCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], tempCaja))
        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=3)
        voltajeBat = bat.values("fecha", "valor", "pozo")
        voltajeBat = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], voltajeBat))
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=3)
        humCaja = humC.values("fecha","valor", "pozo")
        humCaja = list(map(lambda datos: [datos["fecha"], datos["valor"], datos["pozo"]], humCaja))     
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
    except:
        variables = {}
    return JsonResponse(variables)

@csrf_exempt
def json_estado(request):
    p = TomaDatos.objects.get(pk=1)
    respuesta={"estado": p.estado}
    print(respuesta)
    return JsonResponse(respuesta)
