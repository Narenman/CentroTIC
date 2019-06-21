from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import re
import json
import time
import numpy
import paho.mqtt.publish as publish

from .forms import UsuariosPrimariosForm, DispositivosForm
from .models import UsuariosPrimarios, Dispositivos, Ciudad, Espectro

# Create your views here.

def index(request):
    respuesta = {}
    return render(request, "bloqueadores/index.html", respuesta)


@login_required
def jamming(request):
    """Para hacer bloqueo manual del espectro"""
    dispositivos = Dispositivos.objects.all()
    dispositivos = dispositivos.values()

    username = "pi"
    password = "raspberry"
    MQTT_broker = "34.74.6.16"

    MQTT_port = 1883
    ins = request.POST

    respuesta = {"dispositivos": dispositivos}
    return render(request, 'bloqueadores/jamming.html',respuesta)


@login_required
def monitoring(request):
    """ Para hacer monitoreo del espectro """
    ciudad_form = UsuariosPrimariosForm()
    cont = dict() #diccionario de control
    dispositivos = Dispositivos.objects.all()
    dispositivos = dispositivos.values()
       
    #seleccion de terminales IoT para enviar instrucciones MQTT
    if request.GET:
        USRPS = request.GET
        keys = USRPS.keys()
        terminales_seleccionados = []
        for k in keys:
            regex = re.findall(r'^[-+]?\d', k)
            if len(regex)>0:
                terminales_seleccionados.append(regex[0])

        print(terminales_seleccionados)
        ##################  MQTT  ##############33
        username = "pi"
        password = "raspberry"
        MQTT_broker = "34.74.6.16"
        MQTT_port = 1883

        # informacion para enviar al USRP
        fft_size = 4096 # fft size,
        samp_rate = 16e6
        frecuencia_central = [96e6, 112e6]
        ganancia = 50
        tiempo_sensado = 1 #segundos
        #mensaje que se enviara a los USRP
        SCAN_REQ = json.dumps({"fft_size": fft_size, "sample_rate": samp_rate, "frec_central": frecuencia_central,
                                "ganancia": ganancia, "tiempo_sensado": tiempo_sensado, "accion": "monitorear-espectro"})
        #creacion de las instrucciones para enviar por MQTT a traves de los topicos
        msg = []
        for i in range(len(terminales_seleccionados)):
            dispositivo = Dispositivos.objects.get(pk=int(terminales_seleccionados[i]))
            topico = dispositivo.modelo_id + dispositivo.ubicacion + str(dispositivo.pk)
            print(topico)
            msg.append((topico, SCAN_REQ, 2))

        #publicacion de los mensajes MQTT a los dispositivos seleccionados por los clientes
        publish.multiple(msg, hostname=MQTT_broker, port=MQTT_port, auth={"username": username, "password": password})

        # aca se debe esperar un tiempo a que los dispositivos reporten la informacion a la base de datos

        # se lee el espectro y se llama la funcion para procesarlo
    
    cont.update({"ciudad_form": ciudad_form, "dispositivos":dispositivos})
    return render(request, "bloqueadores/monitoring.html", cont)

def consulta_usuarios_primarios(request):
    usuarios_primarios = UsuariosPrimariosForm()
    if request.POST:
        dato_cliente = request.POST
        usuarios = UsuariosPrimarios.objects.filter(ciudad_id=dato_cliente["ciudad"])
        usuarios = usuarios.values("nombre_emisora", "clase_emisora", "frecuencia")
        respuesta = {"usuarios_primarios": usuarios_primarios, "usuarios": usuarios}
    else:
        respuesta = {"usuarios_primarios": usuarios_primarios}
    return render(request, "bloqueadores/consulta_usuarios_primarios.html", respuesta)

def registrar_dispositivos(request):
    dispositivos = DispositivosForm()
    # print(request.POST)
    if request.POST:
        dispositivos = DispositivosForm(request.POST)
        if dispositivos.is_valid():
            dispositivos.save()
            return render(request,"bloqueadores/index.html",{"registrado":"Dispositivo registrado"})
    respuesta = {"dispositivos": dispositivos}
    return render(request, "bloqueadores/registrar_dispositivos.html", respuesta)

def consulta_dispositivos(request):
    dispositivos = Dispositivos.objects.all()
    dispositivos = dispositivos.values("modelo_id", "ubicacion", "ciudad")
    for lista_ciudad in dispositivos:
        ciudad = Ciudad.objects.get(pk=lista_ciudad["ciudad"])
        lista_ciudad.update({"ciudad":ciudad})
    return render(request,"bloqueadores/consulta_dispositivos.html",{"dispositivos": dispositivos})

@csrf_exempt
def espectro_json(request):
    """Esto es solo con fines de graficar los datos recolectados por dispositivo"""

    #aca debo hacer la consulta de dispositivos registrados
    try:
        #lectura de datos de la base de datos filtrada por dispositivos
        espectro  = Espectro.objects.filter(dispositivo=1)
        espectro = espectro.values("espectro_iq", "frec_central", "samp_rate", "fft_size")
        y = numpy.array([])
        #concatenacion de los datos recolectados por las frecuencias centrales diferentes
        for dato in espectro:
            print(dato["frec_central"])
            fft_size = dato["fft_size"]
            x = dato["espectro_iq"]
            y = numpy.append(y, x[0:fft_size])
            samp_rate = dato["samp_rate"]
        f = numpy.arange(0, len(y), 1)*samp_rate/fft_size+88e6 # creacion del vector de frecuencias
        # datos enviados al javascript para que realize la grafica del espectro
        spectrum = list(map(lambda f, Pxx : [f/1e6, Pxx], f, y))
        respuesta = {"spectrum":spectrum}
    except:
        respuesta = {}
    return JsonResponse(respuesta)


def grafica_espectro(request):
    return render(request, "bloqueadores/grafica_espectro.html", {})