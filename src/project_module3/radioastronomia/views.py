import paho.mqtt.publish as publish
import json
import numpy
import time

from .models import AlbumImagenes, Espectro, Estado, CaracteristicasAntena, CaracteristicasEstacion
from .forms import EspectroForm, RFIForm

from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

# Create your views here.
def publishMQTT(topico, msg):
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    publish.single(topico, msg, port=1883, hostname=IP_broker,
     auth={"username": usuario_broker, "password":password_broker})

def index(request):
    return render(request, "radioastronomia/index.html", {})

def json_spectro(request):
    """Se encarga retornar los valores que muestra el espectro
    en el navegador """
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
            time.sleep(3)
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
