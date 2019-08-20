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
    IP_broker = "35.243.199.245"
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
    IP_broker = "35.243.199.245"
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
    try:
        temp = Temperatura.objects.filter(pozo_id=1)
        temp = temp.last()
        temp_largo=Temperatura.objects.filter(pozo_id=1).count()
        temp_last18=Temperatura.objects.filter(pozo_id=1)[temp_largo-18:]
        temperatura18_value = temp_last18.values("valor")
        acum_temp=0
        for x in range(0, 18):
            temp_value=temperatura18_value[x]["valor"]
            #print(temp_value)
            acum_temp=acum_temp+temp_value
        temp_average=round(acum_temp/18,2)
        temperatura = [temp.fecha, temp.valor, temp_average]
        
        #oxígeno disuelto
        od = O2disuelto.objects.filter(pozo_id=1)
        od = od.last()
        od_largo=O2disuelto.objects.filter(pozo_id=1).count()
        od_last18=O2disuelto.objects.filter(pozo_id=1)[od_largo-18:]
        od18_value = od_last18.values("valor")
        acum_od=0
        for x in range(0, 18):
            od_value=od18_value[x]["valor"]
            #print(temp_value)
            acum_od=acum_od+od_value
        od_average=round(acum_od/18,2)
        oxigenoDisuelto = [od.fecha, od.valor, od_average]
        
        #ph
        ph = PH.objects.filter(pozo_id=1)
        ph = ph.last()
        ph_largo=PH.objects.filter(pozo_id=1).count()
        ph_last18=PH.objects.filter(pozo_id=1)[ph_largo-18:]
        ph18_value = ph_last18.values("valor")
        acum_ph=0
        for x in range(0, 18):
            ph_value=ph18_value[x]["valor"]
            #print(temp_value)
            acum_ph=acum_ph+ph_value
        ph_average=round(acum_ph/18,2)
        phTank = [ph.fecha, ph.valor, ph_average]
        
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=1)
        tempC = tempC.last()
        tempC_largo=TemperaturaCaja.objects.filter(pozo_id=1).count()
        tempC_last18=TemperaturaCaja.objects.filter(pozo_id=1)[tempC_largo-18:]
        temperaturaC18_value = tempC_last18.values("valor")
        acum_tempC=0
        for x in range(0, 18):
            tempC_value=temperaturaC18_value[x]["valor"]
            #print(temp_value)
            acum_tempC=acum_tempC+tempC_value
        tempC_average=round(acum_tempC/18,2)
        tempCaja = [tempC.fecha, tempC.valor, tempC_average]

        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=1)
        bat = bat.last()
        bat_largo=VoltajeBateria.objects.filter(pozo_id=1).count()
        bat_last18=VoltajeBateria.objects.filter(pozo_id=1)[bat_largo-18:]
        bat18_value = bat_last18.values("valor")
        acum_bat=0
        for x in range(0, 18):
            bat_value=bat18_value[x]["valor"]
            #print(temp_value)
            acum_bat=acum_bat+bat_value
        bat_average=round(acum_bat/18,2)
        voltajeBat = [bat.fecha, bat.valor, bat_average]
        
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=1)
        humC = humC.last()
        humC_largo=HumedadCaja.objects.filter(pozo_id=1).count()
        humC_last18=HumedadCaja.objects.filter(pozo_id=1)[humC_largo-18:]
        humC18_value = humC_last18.values("valor")
        acum_humC=0
        for x in range(0, 18):
            humC_value=humC18_value[x]["valor"]
            #print(temp_value)
            acum_humC=acum_humC+humC_value
        humC_average=round(acum_humC/18,2)
        humCaja = [humC.fecha, humC.valor, humC_average]
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
        # print(variables)
    except:
        variables = {}
    return JsonResponse(variables)

@csrf_exempt
def json_last_est2(request):
    try:
        temp = Temperatura.objects.filter(pozo_id=2)
        temp = temp.last()
        temp_largo=Temperatura.objects.filter(pozo_id=2).count()
        temp_last18=Temperatura.objects.filter(pozo_id=2)[temp_largo-5:]
        temperatura18_value = temp_last18.values("valor")
        acum_temp=0
        for x in range(0, 18):
            temp_value=temperatura18_value[x]["valor"]
            #print(temp_value)
            acum_temp=acum_temp+temp_value
        temp_average=round(acum_temp/18,2)
        temperatura = [temp.fecha, temp.valor, temp_average]
        
        #oxígeno disuelto
        od = O2disuelto.objects.filter(pozo_id=2)
        od = od.last()
        od_largo=O2disuelto.objects.filter(pozo_id=2).count()
        od_last18=O2disuelto.objects.filter(pozo_id=2)[od_largo-5:]
        od18_value = od_last18.values("valor")
        acum_od=0
        for x in range(0, 18):
            od_value=od18_value[x]["valor"]
            #print(temp_value)
            acum_od=acum_od+od_value
        od_average=round(acum_od/18,2)
        oxigenoDisuelto = [od.fecha, od.valor, od_average]
        
        #ph
        ph = PH.objects.filter(pozo_id=2)
        ph = ph.last()
        ph_largo=PH.objects.filter(pozo_id=2).count()
        ph_last18=PH.objects.filter(pozo_id=2)[ph_largo-5:]
        ph18_value = ph_last18.values("valor")
        acum_ph=0
        for x in range(0, 18):
            ph_value=ph18_value[x]["valor"]
            #print(temp_value)
            acum_ph=acum_ph+ph_value
        ph_average=round(acum_ph/18,2)
        phTank = [ph.fecha, ph.valor, ph_average]
        
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=2)
        tempC = tempC.last()
        tempC_largo=TemperaturaCaja.objects.filter(pozo_id=2).count()
        tempC_last18=TemperaturaCaja.objects.filter(pozo_id=2)[tempC_largo-5:]
        temperaturaC18_value = tempC_last18.values("valor")
        acum_tempC=0
        for x in range(0, 18):
            tempC_value=temperaturaC18_value[x]["valor"]
            #print(temp_value)
            acum_tempC=acum_tempC+tempC_value
        tempC_average=round(acum_tempC/18,2)
        tempCaja = [tempC.fecha, tempC.valor, tempC_average]

        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=2)
        bat = bat.last()
        bat_largo=VoltajeBateria.objects.filter(pozo_id=2).count()
        bat_last18=VoltajeBateria.objects.filter(pozo_id=2)[bat_largo-5:]
        bat18_value = bat_last18.values("valor")
        acum_bat=0
        for x in range(0, 18):
            bat_value=bat18_value[x]["valor"]
            #print(temp_value)
            acum_bat=acum_bat+bat_value
        bat_average=round(acum_bat/18,2)
        voltajeBat = [bat.fecha, bat.valor, bat_average]
        
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=2)
        humC = humC.last()
        humC_largo=HumedadCaja.objects.filter(pozo_id=2).count()
        humC_last18=HumedadCaja.objects.filter(pozo_id=2)[humC_largo-5:]
        humC18_value = humC_last18.values("valor")
        acum_humC=0
        for x in range(0, 18):
            humC_value=humC18_value[x]["valor"]
            #print(temp_value)
            acum_humC=acum_humC+humC_value
        humC_average=round(acum_humC/18,2)
        humCaja = [humC.fecha, humC.valor, humC_average]
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
    except:
        variables = {}
    return JsonResponse(variables)

def json_last_est3(request):
    try:
        temp = Temperatura.objects.filter(pozo_id=3)
        temp = temp.last()
        temp_largo=Temperatura.objects.filter(pozo_id=3).count()
        temp_last18=Temperatura.objects.filter(pozo_id=3)[temp_largo-5:]
        temperatura18_value = temp_last18.values("valor")
        acum_temp=0
        for x in range(0, 18):
            temp_value=temperatura18_value[x]["valor"]
            #print(temp_value)
            acum_temp=acum_temp+temp_value
        temp_average=round(acum_temp/18,2)
        temperatura = [temp.fecha, temp.valor, temp_average]
        
        #oxígeno disuelto
        od = O2disuelto.objects.filter(pozo_id=3)
        od = od.last()
        od_largo=O2disuelto.objects.filter(pozo_id=3).count()
        od_last18=O2disuelto.objects.filter(pozo_id=3)[od_largo-5:]
        od18_value = od_last18.values("valor")
        acum_od=0
        for x in range(0, 18):
            od_value=od18_value[x]["valor"]
            #print(temp_value)
            acum_od=acum_od+od_value
        od_average=round(acum_od/18,2)
        oxigenoDisuelto = [od.fecha, od.valor, od_average]
        
        #ph
        ph = PH.objects.filter(pozo_id=3)
        ph = ph.last()
        ph_largo=PH.objects.filter(pozo_id=3).count()
        ph_last18=PH.objects.filter(pozo_id=3)[ph_largo-5:]
        ph18_value = ph_last18.values("valor")
        acum_ph=0
        for x in range(0, 18):
            ph_value=ph18_value[x]["valor"]
            #print(temp_value)
            acum_ph=acum_ph+ph_value
        ph_average=round(acum_ph/18,2)
        phTank = [ph.fecha, ph.valor, ph_average]
        
        #temperatura caja
        tempC = TemperaturaCaja.objects.filter(pozo_id=3)
        tempC = tempC.last()
        tempC_largo=TemperaturaCaja.objects.filter(pozo_id=3).count()
        tempC_last18=TemperaturaCaja.objects.filter(pozo_id=3)[tempC_largo-5:]
        temperaturaC18_value = tempC_last18.values("valor")
        acum_tempC=0
        for x in range(0, 18):
            tempC_value=temperaturaC18_value[x]["valor"]
            #print(temp_value)
            acum_tempC=acum_tempC+tempC_value
        tempC_average=round(acum_tempC/18,2)
        tempCaja = [tempC.fecha, tempC.valor, tempC_average]

        #voltaje batería
        bat=VoltajeBateria.objects.filter(pozo_id=3)
        bat = bat.last()
        bat_largo=VoltajeBateria.objects.filter(pozo_id=3).count()
        bat_last18=VoltajeBateria.objects.filter(pozo_id=3)[bat_largo-5:]
        bat18_value = bat_last18.values("valor")
        acum_bat=0
        for x in range(0, 18):
            bat_value=bat18_value[x]["valor"]
            #print(temp_value)
            acum_bat=acum_bat+bat_value
        bat_average=round(acum_bat/18,2)
        voltajeBat = [bat.fecha, bat.valor, bat_average]
        
        #humedad caja
        humC = HumedadCaja.objects.filter(pozo_id=3)
        humC = humC.last()
        humC_largo=HumedadCaja.objects.filter(pozo_id=3).count()
        humC_last18=HumedadCaja.objects.filter(pozo_id=3)[humC_largo-5:]
        humC18_value = humC_last18.values("valor")
        acum_humC=0
        for x in range(0, 18):
            humC_value=humC18_value[x]["valor"]
            #print(temp_value)
            acum_humC=acum_humC+humC_value
        humC_average=round(acum_humC/18,2)
        humCaja = [humC.fecha, humC.valor, humC_average]
        variables = {"temperatura":temperatura, "oxigenoDisuelto": oxigenoDisuelto, "phTank": phTank, "tempCaja": tempCaja, "voltajeBat": voltajeBat, "humCaja": humCaja}
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
