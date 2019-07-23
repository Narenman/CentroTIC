from django.shortcuts import render
from .models import AlbumImagenes, Espectro
from django.http import JsonResponse
import numpy
# from imageupload.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.

def index(request):
    return render(request, "radioastronomia/index.html", {})

def json_spectro(request):

    try:
        espectro = Espectro.objects.last()
        nfft = espectro.nfft
        frec_central = espectro.frec_central
        frec_muestreo = espectro.frec_muestreo
        print(frec_muestreo)
        espectro = espectro.espectro
        espectro = numpy.asarray(espectro)
        # promediado del espectro
        K = 2
        x = numpy.zeros(nfft)
        for i in range(K):
            x = x + espectro[i*nfft:(i+1)*nfft]
        x = x/K
        frec = (numpy.arange(0,nfft,1)*frec_muestreo/nfft + frec_central/2)/1e6 #puntos espectrales
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
        respuesta = {"imagenes": album}
    except:
        respuesta = {}
                
    return render(request, "radioastronomia/control_manual.html", respuesta)