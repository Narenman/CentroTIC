import paho.mqtt.publish as publish
import json
import numpy
import time
import pandas as pd

from .models import AlbumImagenes, Espectro, Estado, CaracteristicasAntena, \
                    CaracteristicasEstacion, RBW, CaracteristicasEspectro
from .forms import EspectroForm, RFIForm, RegionForm

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

# Create your views here.
def publishMQTT(topico, msg):
    """ Se encarga de establecer comunicacion
    MQTT con los dispositivos """
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    publish.single(topico, msg, port=1883, hostname=IP_broker,
     auth={"username": usuario_broker, "password":password_broker})

def promedio(espectro, nfft):
    """ Realiza promedios del espectro,
    debido a que las muestras estan almacenadas en un vector de tamano N
    que se subdivide N/nfft veces y ese es el numero que se promedia (K)"""
    K = int(len(espectro)/(nfft))
    x = numpy.zeros(nfft)
    for i in range(K):
        x = x + espectro[i*nfft:(i+1)*nfft]
    x = x/K
    return x   

def bandas_espectrales(request):
    region = RegionForm()
    rbw = RBW.objects.all().distinct("rbw") #para obtener los RBW disponibles
    
    respuesta = {"region": region, "rbw":rbw}
    return render(request, "radioastronomia/bandas_espectrales.html",respuesta)

#modos de operacion del espectro
@csrf_exempt
def barrido_json(request):
    respuesta = dict()
    if request.POST:
        try:
            cliente = request.POST
            print(cliente)
            # try:
            # analisis RF
            #obtener frecuencia de muestreo y nfft
            resBW = RBW.objects.get(rbw=cliente["RBW"])
            frec_muestreo = resBW.frecuencia_muestreo
            nfft = resBW.nfft
            #filtrado para obtener cada banda
            frec_central = Espectro.objects.filter(nfft=nfft).filter(frec_muestreo=frec_muestreo).distinct("frec_central")
            frec_central = frec_central.values("frec_central")
            y = numpy.array([])
            #ahora se obtiene el espectro por cada banda espectral
            freq = []
            fechas = []
            char_energia = []
            for f in frec_central:
                rows = Espectro.objects.filter(nfft=nfft).filter(frec_muestreo=frec_muestreo).filter(frec_central__exact=f["frec_central"])
                rows = rows.values("id","fecha", "espectro")
                x_ = numpy.zeros(nfft)
                for row in rows:
                    espectro = row["espectro"]
                    espectro = numpy.asarray(espectro)
                    x = promedio(espectro, nfft)
                    x_ = x_ + x
                    x_ = x_/len(rows)
                    y = numpy.append(y, x_)
                    fechas.append(row["fecha"].day)

                freq.append(f["frec_central"])  
            
                
                #analsis caracteristicas de la energia
                ids = Espectro.objects.filter(frec_central=f["frec_central"])
                ids = ids.values("id")
                car_energia =CaracteristicasEspectro.objects.filter(espectro__in=ids)
                car_energia = car_energia.values("energia")
                
                mu = 0
                for row in car_energia:
                    energia = row["energia"]
                    energia = numpy.asarray(energia)
                    mu = mu + numpy.mean(energia)
                mu = mu/len(car_energia)
                mu = 10*numpy.log10(mu)
                char_energia.append(mu)
            #organizacion de los datos para las graficas
            data_energia = []
            for i in range(len(freq)):
                data_energia.append([freq[i]/1000000, char_energia[i]])

            freq = numpy.linspace(min(freq), max(freq), len(y)) #vector de las frecuencias
            data = []
            for j in range(len(freq)):
                data.append([freq[j]/1000000.0, y[j]])
            
            print(len(fechas))
            respuesta.update({"datos": len(y), "lenf": len(freq),
                                "data": data, "data_energia": data_energia})
        except:
            respuesta = {"datos": "no existen lecturas"}
    return JsonResponse(respuesta)

def json_spectro(request):
    """Se encarga retornar los valores que muestra el espectro
    en el navegador para el modo manual"""
    try:
        espectro = Espectro.objects.last()
        nfft = espectro.nfft
        frec_central = espectro.frec_central
        frec_muestreo = espectro.frec_muestreo
        print(frec_muestreo)
        espectro = espectro.espectro
        espectro = numpy.asarray(espectro)
        # promediado del espectro
        K = int(len(espectro)*2/(nfft*3))
        print(K, "K")
        x = numpy.zeros(nfft)
        for i in range(K):
            x = x + espectro[i*nfft:(i+1)*nfft]
        x = x/K
        frec = (numpy.arange(-int(nfft/2),int(nfft/2),1)*frec_muestreo/nfft + frec_central)/1e6 #puntos espectrales
        
        #organizacion de los datos para que javascript los pueda interpretar
        respuesta = []
        for i in range(nfft):
            respuesta.append([frec[i], x[i]])
    except:
        respuesta = {}
    return JsonResponse({"espectro":respuesta})

def control_manual(request):
    """ Es para mostrar la interfaz del control manual del espectro """
    try:
        album = AlbumImagenes.objects.last()
        album = album.imagen
        form = EspectroForm()
        
        respuesta = dict()
        estado = Estado.objects.get(pk=1)
        if estado.activo == True:
            respuesta.update({"estado":"activo"})

        if request.POST:
            print(request.POST)
            cliente = request.POST
            msg = {"nfft": int(cliente["nfft"]), "sample_rate": int(cliente["frec_muestreo"]),
            "ganancia": 50, "duracion": 5, "frec_central": int(cliente["frec_central"]),
            "accion": "modo manual", "region": cliente["region"]}
            topico = "radioastronomia/RFI"

            #envio de la instruccion al subsistema RFI
            publishMQTT(topico, json.dumps(msg))
            time.sleep(3)
            estado = Estado.objects.get(pk=1)
            if estado.activo == True:
                respuesta.update({"estado":"activo"})
        respuesta.update({"imagenes": album, "form": form})
    except:
        form = EspectroForm()
        respuesta = {"form":form}              
    return render(request, "radioastronomia/control_manual.html", respuesta)

def control_automatico(request):
    try:
        form = RFIForm()
        respuesta = dict()
        estado = Estado.objects.get(pk=1)
        if estado.activo == True:
            respuesta.update({"estado":"activo"})

        if request.POST:
            cliente = request.POST
            print(cliente)
            msg = {"nfft": int(cliente["nfft"]), "sample_rate": int(cliente["frecuencia_muestreo"]),
            "ganancia": 50, "duracion": 2, "frecuencia_inicial": int(cliente["frecuencia_inicial"]),
            "accion": "modo automatico", "region": 1, "frecuencia_final": int(cliente["frecuencia_final"])}
            topico = "radioastronomia/RFI"
            #envio de la instruccion al subsistema RFI
            publishMQTT(topico, json.dumps(msg))
            time.sleep(5)
            estado = Estado.objects.get(pk=1)
            if estado.activo == True:
                respuesta.update({"estado":"activo"})
        respuesta.update({"form": form})
    except:
        form = RFIForm()
        respuesta = {"form": form}
    return render(request, "radioastronomia/control_automatico.html", respuesta)

# Informacion adicional de antenas utilizadas
class CaracteristicasAntenaListView(ListView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_list.html"
    context_object_name = "caracteristicasantena"

class CaracteristicasAntenaCreateView(CreateView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_create.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:antenas")

class CaracteristicasAntenaUpdateView(UpdateView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_update.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:antenas")

class CaracteristicasAntenaDeleteView(DeleteView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_delete.html"
    success_url = reverse_lazy("radioastronomia:antenas")
    context_object_name = "caracteristicasantena"

#informacion adicional de la estacion de monitoreo
class CaracteristicasEstacionListView(ListView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_list.html"
    context_object_name="caractestacion"

class CaracteristicasEstacionCreateView(CreateView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_create.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:subsistema-estacion")

class CaracteristicasEstacionUpdateView(UpdateView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_update.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:subsistema-estacion")

class CaracteristicasEstacionDeleteView(DeleteView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_delete.html"
    context_object_name = "caracterstacion"
    success_url = reverse_lazy("radioastronomia:subsistema-estacion")

# # informacion sobre las resoluciones espectrales

class RBWListView(ListView):
    model = RBW
    template_name = "radioastronomia/rbw_list.html"
    context_object_name="rbw"

class RBWCreateView(CreateView):
    model = RBW
    template_name = "radioastronomia/rbw_create.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:rbw")



