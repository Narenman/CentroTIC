from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

from .models import Analisis, Lecturas, DatosEvaluar
from .forms import EntrenamientoForm, AnalisisForm, Seleccion_entrenamientoForm

import paho.mqtt.publish as publish
import pandas as pd
import time
import json
import csv
import os


# Create your views here.
def index(request):
    respuesta = {}
    return render(request, "nariz_electronica/index.html", respuesta)

@login_required
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


@login_required
def analisis_nariz(request):
    """ Recolecta los parametros de configuracion de la nariz electronica para realizar el sensado
    """
    analisis = AnalisisForm()
    if request.POST:
        analisis = AnalisisForm(request.POST,)
        accion = {}
        req = request.POST
        if analisis.is_valid() and float(req["tiempo_medicion_segundos"])<360 and float(req["tiempo_medicion_segundos"])>0:
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
            IP_broker = "35.243.199.245"
            usuario_broker = "pi"
            password_broker = "raspberry"
            publish.single(topico, accion, port=1883, hostname=IP_broker,
             auth={"username": usuario_broker, "password":password_broker})

            return render(request, "nariz_electronica/toma_datos.html", {"analisis_confirmacion": "Analisis ejecutado en la nariz electronica"})

    respuesta = {"analisis": analisis}
    return render(request, "nariz_electronica/analisis.html", respuesta)

def recolectar_datos_entrenamiento(request):
    """Retorna un archivo .csv con los datos recolectados de la nariz
    """
    analisis = Seleccion_entrenamientoForm()
    if request.POST:
        datos = request.POST
        datos = int(datos["entrenamiento"]) # corresponde al dato del formulario para filtrar
        analisis_datos = Analisis.objects.filter(entrenamiento=datos) # busca los analisis asociados al entrenamiento
        lecturas = Lecturas.objects.filter(analisis__in=analisis_datos) # extrae las lecturas asociadas a los analisis
        #organizacion de la informacion
        analisis_exp = list(map(lambda analisis_datos: [analisis_datos.nombre, analisis_datos.pk] ,analisis_datos))
        datos_entrenamiento = list(map(lambda lecturas: lecturas.medicion ,lecturas))
        etiquetas = list(map(lambda lecturas: lecturas.analisis ,lecturas))
         # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="datos.csv"'
        writer = csv.writer(response)
        for i in range(len(datos_entrenamiento)):
            writer.writerow([datos_entrenamiento[i], analisis_exp[i]])
        return response  

    respuesta = {"analisis": analisis}
    return render(request, "nariz_electronica/seleccion_entrenamiento.html", respuesta)

def toma_datos(request):
    """ Es la interfaz para recolectar los datos del entrenamiento o para registrar el analisis """
    return render(request, "nariz_electronica/toma_datos.html", {})

#existen 6 casos de uso de aplicaciones de la nariz electronica
def evaluacion_clasificadores(request):
    # lecturas = Lecturas.objects.last()
    # datos = lecturas.medicion
    # lista_sensores = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"]
    # datos = pd.DataFrame(data=datos, columns=lista_sensores)
    # print(datos)
    return render(request, "nariz_electronica/evaluacion_clasificadores.html",{})

# para la version 1 de la nariz
# necesitamos deteccion de maderas, rocas y triatominos
def clasificacion_maderas(request):
    """Esta vista se encarga pasar el dato recolectado por la nariz electronica v1 y evaluarlo con 
    el modelo entrenado para la nariz """

    #envio de informacion a la nariz para que inicie el escaneo de la muestra
    topico = "UIS/NARIZ/PRINCIPAL"
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    accion = {"accion": "clasificacion-datos"}
    publish.single(topico, json.dumps(accion), port=1883, hostname=IP_broker,
    auth={"username": usuario_broker, "password":password_broker})

    #se necesita pausar el servidor mientras llegan nuevos datos a la base de datos
    time.sleep(1)
    #despues de enviar los datos se realiza la consulta
    try:
        lecturas = DatosEvaluar.objects.last()
        lecturas = lecturas.medicion
        lista_sensores = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"]
        datos = pd.DataFrame(data=lecturas, columns=lista_sensores)
        """ Aqui se carga el codigo de la clasificacion """
        from sklearn.externals import joblib
        # se determina la ruta de almacenamiento
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BASE_DIR = os.path.join(BASE_DIR,"nariz_electronica/modelos_entrenados")
        # se lee el modelo entrenado 
        clasificador = joblib.load(BASE_DIR+'/svm1_corr.pkl')
        # se evalua el modelo con los datos recolectados por la nariz,
        # en este caso solo son 10 porque el modelo que tengo solo tiene 10 sensores pero deben ser 16
        resultado = clasificador.predict(datos[["S1","S2","S3","S4", "S5", "S6","S7","S8","S9","S10"]])

        # en esta parte se colocan las clases de clasificacion
        clases = ["Illegal","Testing"]
        # por cada muestra de los datos se evalua la clase en la que esta
        respuesta_cliente = []
        for res in resultado:
            respuesta_cliente.append(clases[res])
        respuesta = {"resultado_clasificacion": respuesta_cliente}

    except:
        respuesta = {}
    return render(request,"nariz_electronica/clasificacion_maderas.html",respuesta)


def clasificacion_rocas(request):
    """Esta vista se encarga pasar el dato recolectado por la nariz electronica v1 y evaluarlo con 
    el modelo entrenado para la nariz """

    #envio de informacion a la nariz para que inicie el escaneo de la muestra
    topico = "UIS/NARIZ/PRINCIPAL"
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    accion = {"accion": "clasificacion-datos"}
    publish.single(topico, json.dumps(accion), port=1883, hostname=IP_broker,
    auth={"username": usuario_broker, "password":password_broker})

    #se necesita pausar el servidor mientras llegan nuevos datos a la base de datos
    time.sleep(1)
    #despues de enviar los datos se realiza la consulta
    try:
        lecturas = DatosEvaluar.objects.last()
        lecturas = lecturas.medicion
        lista_sensores = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"]
        datos = pd.DataFrame(data=lecturas, columns=lista_sensores)
        """ Aqui se carga el codigo de la clasificacion """
        from sklearn.externals import joblib
        # se determina la ruta de almacenamiento
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BASE_DIR = os.path.join(BASE_DIR,"nariz_electronica/modelos_entrenados")
        # se lee el modelo entrenado 
        clasificador = joblib.load(BASE_DIR+'/svm1_corr.pkl')
        # se evalua el modelo con los datos recolectados por la nariz,
        # en este caso solo son 10 porque el modelo que tengo solo tiene 10 sensores pero deben ser 16
        resultado = clasificador.predict(datos[["S1","S2","S3","S4", "S5", "S6","S7","S8","S9","S10"]])

        # en esta parte se colocan las clases de clasificacion
        clases = ["Illegal","Testing"]
        # por cada muestra de los datos se evalua la clase en la que esta
        respuesta_cliente = []
        for res in resultado:
            respuesta_cliente.append(clases[res])
        respuesta = {"resultado_clasificacion": respuesta_cliente}

    except:
        respuesta = {}
    return render(request,"nariz_electronica/clasificacion_maderas.html",respuesta)

def clasificacion_triatominos(request):
    """Esta vista se encarga pasar el dato recolectado por la nariz electronica v1 y evaluarlo con 
    el modelo entrenado para la nariz """

    #envio de informacion a la nariz para que inicie el escaneo de la muestra
    topico = "UIS/NARIZ/PRINCIPAL"
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    accion = {"accion": "clasificacion-datos"}
    publish.single(topico, json.dumps(accion), port=1883, hostname=IP_broker,
    auth={"username": usuario_broker, "password":password_broker})

    #se necesita pausar el servidor mientras llegan nuevos datos a la base de datos
    time.sleep(1)
    #despues de enviar los datos se realiza la consulta
    try:
        lecturas = DatosEvaluar.objects.last()
        lecturas = lecturas.medicion
        lista_sensores = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"]
        datos = pd.DataFrame(data=lecturas, columns=lista_sensores)
        """ Aqui se carga el codigo de la clasificacion """
        from sklearn.externals import joblib
        # se determina la ruta de almacenamiento
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BASE_DIR = os.path.join(BASE_DIR,"nariz_electronica/modelos_entrenados")
        # se lee el modelo entrenado 
        clasificador = joblib.load(BASE_DIR+'/svm1_corr.pkl')
        # se evalua el modelo con los datos recolectados por la nariz,
        # en este caso solo son 10 porque el modelo que tengo solo tiene 10 sensores pero deben ser 16
        resultado = clasificador.predict(datos[["S1","S2","S3","S4", "S5", "S6","S7","S8","S9","S10"]])

        # en esta parte se colocan las clases de clasificacion
        clases = ["Illegal","Testing"]
        # por cada muestra de los datos se evalua la clase en la que esta
        respuesta_cliente = []
        for res in resultado:
            respuesta_cliente.append(clases[res])
        respuesta = {"resultado_clasificacion": respuesta_cliente}

    except:
        respuesta = {}
    return render(request,"nariz_electronica/clasificacion_maderas.html",respuesta)