import paho.mqtt.publish as publish
import json
import numpy

from .models import AlbumImagenes, Espectro
from .forms import EspectroForm, RFIForm

from django.shortcuts import render
from django.http import JsonResponse

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
        if request.POST:
            print(request.POST)
            cliente = request.POST
            msg = {"nfft": int(cliente["nfft"]), "sample_rate": int(cliente["frec_muestreo"]),
            "ganancia": 50, "duracion": 5, "frec_central": int(cliente["frec_central"]),
            "accion": "modo manual", "region": cliente["region"]}
            topico = "radioastronomia/RFI"

            #envio de la instruccion al subsistema RFI
            publishMQTT(topico, json.dumps(msg))
        respuesta = {"imagenes": album, "form": form}
    except:
        form = EspectroForm()
        respuesta = {"form":form}              
    return render(request, "radioastronomia/control_manual.html", respuesta)

def control_automatico(request):
    try:
        form = RFIForm()
        if request.POST:
            cliente = request.POST
            print(cliente)
            msg = {"nfft": int(cliente["nfft"]), "sample_rate": int(cliente["frecuencia_muestreo"]),
            "ganancia": 50, "duracion": 5, "frecuencia_inicial": int(cliente["frecuencia_inicial"]),
            "accion": "modo automatico", "region": 1, "frecuencia_final": int(cliente["frecuencia_final"])}
            topico = "radioastronomia/RFI"

            #envio de la instruccion al subsistema RFI
            publishMQTT(topico, json.dumps(msg))
        respuesta = {"form": form}
    except:
        form = RFIForm()
        respuesta = {"form": form}
    return render(request, "radioastronomia/control_automatico.html", respuesta)