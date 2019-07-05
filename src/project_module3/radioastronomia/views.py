from django.shortcuts import render
from .models import AlbumImagenes
# from imageupload.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.

def index(request):
    return render(request, "radioastronomia/index.html", {})


def control_manual(request):
    album = AlbumImagenes.objects.all()
    respuesta = {"imagenes": album,}
                
    return render(request, "radioastronomia/control_manual.html", respuesta)