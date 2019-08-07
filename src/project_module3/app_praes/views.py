import json
import time
import paho.mqtt.publish as publish
import pandas as pd
import csv
import numpy 

from .models import Temperatura, Humedad, PresionAtmosferica, Ubicacion_lectura, \
    Semillero, Kit, PH_agua, Turbidez_agua, Temperatura_agua, Flujo_agua, KitNariz, Colegio
from .forms import UbicacionForm, UbicacionLecturasForm

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from django.contrib.auth.decorators import login_required
from django.urls import reverse, resolve, reverse_lazy

def publishMQTT(topico, msg):
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    publish.single(topico, msg, port=1883, hostname=IP_broker,
     auth={"username": usuario_broker, "password":password_broker})

# Create your views here.

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
                              "ubicacion": ubicacion})
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


def preparacion(modelo):
    modelo = modelo.values("fecha", "valor")
    df = pd.DataFrame(data=modelo)
    #valores estadisticos de las muestras
    calculo = df.describe()
    calculo = calculo["valor"]
    respuesta = {"Nmuestras": calculo[0], "media": calculo[1],
                 "std": calculo[2], "min":calculo[3], "q1": calculo[4],
                 "q2": calculo[5], "q3": calculo[6], "max": calculo[7]}
    return respuesta

def matematica_ambiental(request):
    form = UbicacionForm()
    if request.POST:
        cliente = request.POST
        print(cliente)
        try:
            if cliente["variable"]=="temperatura":
                modelo = Temperatura.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
                respuesta = preparacion(modelo)
                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo": "temperatura"})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)

            elif cliente["variable"]=="humedad":
                modelo = Humedad.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])   
                respuesta = preparacion(modelo)
                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo": "humedad",})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)

            elif cliente["variable"]=="presion":
                modelo = PresionAtmosferica.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])   
                respuesta = preparacion(modelo)
                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo":"presion"})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)
            
            elif cliente["variable"]=="temp_agua":
                modelo = Temperatura_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])   
                respuesta = preparacion(modelo)
                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo":"temperaturaAgua"})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)
            
            elif cliente["variable"]=="turb_agua":
                modelo = Turbidez_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
                respuesta = preparacion(modelo)
                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo": "turbidezAgua"})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)

            elif cliente["variable"]=="ph_agua":
                modelo = PH_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
                respuesta = preparacion(modelo)
                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo": "PHAgua"})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)
            
            elif cliente["variable"]=="flujo_agua":
                modelo = Flujo_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
                respuesta = preparacion(modelo)
                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo": "flujoAgua"})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)
            
            elif cliente["variable"]=="aire":
                respuesta = dict()

                # aca coloco procesamiento para detectar buenos y malos niveles                
                # modelo = KitNariz.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
                # modelo = modelo.values("fecha", "valor")
                # msg = []
                # for dat in modelo:
                #     msg.append(dat["valor"])
                # columns = ["MQ2", "MQ3", "MQ4", "MQ5", "MQ6", "MQ7", "MQ8", "MQ9", "MQ135", "MICS5524"]
                # df = pd.DataFrame(data=msg, columns=columns)

                respuesta.update({"form": form, "kit_monitoreo":cliente["kit_monitoreo"],
                                  "ubicacion": cliente["ubicacion"], "tipo": "aire"})
                return render(request, "app_praes/matematica_ambiental.html", respuesta)
        except:
            pass

    respuesta = {"form": form}
    return render(request, "app_praes/matematica_ambiental.html", respuesta)


def descargar(request):
    if request.POST:
        cliente = request.POST
        print(cliente["tipo"])
        
        if cliente["tipo"]=="temperatura":
            modelo = Temperatura.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")

        elif cliente["tipo"]=="humedad":
            modelo = Humedad.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")

        elif cliente["tipo"]=="presion":
            modelo = PresionAtmosferica.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")

        elif cliente["tipo"]=="temperaturaAgua":
            modelo = Temperatura_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")        

        elif cliente["tipo"]=="turbidezAgua":
            modelo = Turbidez_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")

        elif cliente["tipo"]=="PHAgua":
            modelo = PH_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")

        elif cliente["tipo"]=="flujoAgua":
            modelo = Flujo_agua.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")
        
        elif cliente["tipo"]=="aire":
            modelo = KitNariz.objects.filter(kit_monitoreo=cliente["kit_monitoreo"]).filter(ubicacion=cliente["ubicacion"])
            modelo = modelo.values("fecha", "valor")
            msg = []
            for dat in modelo:
                msg.append(dat["valor"])
            columns = ["MQ2", "MQ3", "MQ4", "MQ5", "MQ6", "MQ7", "MQ8", "MQ9", "MQ135", "MICS5524"]
            df = pd.DataFrame(data=msg, columns=columns)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="datos.csv"'
            df.to_csv(path_or_buf=response, index=None, header=True)

        if cliente["tipo"]=="temperatura" or cliente["tipo"]=="humedad" or cliente["tipo"]=="presion" or \
            cliente["tipo"]=="temperaturaAgua" or cliente["tipo"]=="turbidezAgua" or \
            cliente["tipo"]=="PHAgua" or cliente["tipo"]=="flujoAgua":

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="datos.csv"'
            writer = csv.writer(response)
            header = ["fecha", "valor"]
            writer.writerow(header)
            for dato in modelo:
                writer.writerow([dato["fecha"], dato["valor"]])
                
    return response

#CRD para la Ubicacion
@method_decorator(login_required, name='dispatch')
class Ubicacion_lecturaCreateView(CreateView):
    """ no necesita ningun formulario """
    model = Ubicacion_lectura
    template_name = "app_praes/registrar_lugar1.html"
    fields = ["etiqueta_ubicacion", "tipo_experimento", "semillero"]
    success_url = reverse_lazy("app_praes:lugares")

class Ubicacion_lecturaListView(ListView):
    """lista la base de datos"""
    model = Ubicacion_lectura
    template_name = "app_praes/ubicacion_lectura_list.html"
    context_object_name = 'ubicaciones'  

class Ubicacion_lecturaDeleteView(DeleteView):
    """permite borrar la base de datos con la url """
    model = Ubicacion_lectura
    context_object_name = 'ubicaciones'
    template_name = "app_praes/del_ubicacion_lectura.html"
    success_url = reverse_lazy("app_praes:lugares")

#CRUD para semillero
@method_decorator(login_required, name='dispatch')
class SemilleroListView(ListView):
    model = Semillero
    template_name = "app_praes/semillero_list.html"
    context_object_name = "semillero"

class SemilleroDeleteView(DeleteView):
    model = Semillero
    template_name = "app_praes/semillero_del.html"
    success_url = reverse_lazy("app_praes:semilleros")

class SemilleroCreateView(CreateView):
    model = Semillero
    template_name = "app_praes/semillero_crear.html"
    fields = "__all__"
    success_url = reverse_lazy("app_praes:semilleros")

#CRUD para colegios
class ColegioListView(ListView):
    model = Colegio
    template_name = "app_praes/colegio_list.html"
    context_object_name="colegio"

class ColegioCreateView(CreateView):
    model = Colegio
    template_name = "app_praes/colegio_crear.html"
    fields = "__all__"
    success_url = reverse_lazy("app_praes:colegios")

class ColegioUpdateView(UpdateView):
    model = Colegio
    fields = "__all__"
    template_name = "app_praes/colegio_update.html"
    success_url = reverse_lazy("app_praes:colegios")

#CRUD para KITS
class KitListView(ListView):
    model = Kit
    template_name = "app_praes/kit_list.html"
    context_object_name="kit"

class KitCreateView(CreateView):
    model = Kit
    template_name = "app_praes/kit_crear.html"
    fields = "__all__"
    success_url = reverse_lazy("app_praes:consulta-kits")

