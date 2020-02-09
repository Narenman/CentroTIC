from django.shortcuts import render
from .models import PMS5003A, PMS5003B
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "particulado/index.html",{})

def json_pmsA(request):
    try:
        pmsa = PMS5003A.objects.all()
        pmsa = pmsa.values("muestra", "dato1", "dato2", "dato3", "id")
        pmsa = list(map(lambda datos: [datos["muestra"], datos["dato1"], datos["dato2"],datos["dato3"],datos["id"]], pmsa))
        respuesta = {"pmsA": pmsa}
    except:
        respuesta = {}
    return JsonResponse(respuesta)

def json_pmsB(request):
    try:
        pmsa = PMS5003B.objects.all()
        pmsa = pmsa.values("muestra", "dato1", "dato2", "dato3","temp","hum", "id")
        pmsa = list(map(lambda datos: [datos["muestra"], datos["dato1"], datos["dato2"],datos["dato3"],datos["temp"],datos["hum"],datos["id"]], pmsa))
        respuesta = {"pmsB": pmsa}
    except:
        respuesta = {}
    return JsonResponse(respuesta)
