from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EntrenamientoForm, AnalisisForm, Seleccion_entrenamientoForm
from django.urls import reverse
from .models import Analisis, Lecturas
from django.http import JsonResponse

import paho.mqtt.publish as publish
import time
import json

# Create your views here.
def index(request):
    respuesta = {}
    return render(request, "nariz_electronica/index.html", respuesta)


def entrenamiento(request):
    """esta vista es para el formulario de entrenamiento 
    general
    """
    entrenamiento = EntrenamientoForm()
    if request.POST:
        entrenamiento = EntrenamientoForm(request.POST)

        if entrenamiento.is_valid():
            entrenamiento.save()
            return HttpResponseRedirect(reverse('nariz_electronica:analisis_nariz'))

    respuesta = {"entrenamiento": entrenamiento}
    return render(request, "nariz_electronica/entrenamiento.html", respuesta)

def analisis_nariz(request):
    """ Recolecta los parametros de configuracion de la nariz electronica para realizar el sensado
    """
    analisis = AnalisisForm()
    if request.POST:
        analisis = AnalisisForm(request.POST,)
        accion = {}
        req = request.POST
        if analisis.is_valid() and float(req["tiempo_medicion_segundos"])<60 and float(req["tiempo_medicion_segundos"])>0:
            analisis.save()
            datos_form = request.POST
            tiempo_medicion = float(datos_form["tiempo_medicion_segundos"])
            entrenamiento = int(datos_form["entrenamiento"])

            model_analisis = Analisis.objects.all().latest('id')
            accion.update({"tiempo": tiempo_medicion, "entrenamiento": entrenamiento, "id": model_analisis.pk, "accion": "adquirir-datos"})
            accion = json.dumps(accion)

            """ Aca va el codigo de MQTT para controlar la nariz electronica
            """

            topico = "UIS/NARIZ/PRINCIPAL"
            IP_broker = "34.73.25.149"
            usuario_broker = "pi"
            password_broker = "raspberry"
            publish.single(topico, accion, port=1883, hostname=IP_broker,
             auth={"username": usuario_broker, "password":password_broker})

            return render(request, "nariz_electronica/index.html", {"analisis_confirmacion": "Analisis ejecutado en la nariz electronica"})

    respuesta = {"analisis": analisis}
    return render(request, "nariz_electronica/analisis.html", respuesta)

def recolectar_datos_entrenamiento(request):
    analisis = Seleccion_entrenamientoForm()
    if request.POST:
        datos = request.POST
        print(datos)
        return JsonResponse({})
    respuesta = {"analisis": analisis}
    return render(request, "nariz_electronica/seleccion_entrenamiento.html", respuesta)