from django.shortcuts import render
from .models import PMS5003A, PMS5003B
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "particulado/index.html",{})

def json_pmsA(request):
    try:
        pmsa = PMS5003A.objects.last()
        print(pmsa.muestra)
        respuesta = {"pmsA": pmsa.muestra, "dato1": pmsa.dato1,
                    "dato2": pmsa.dato2, "dato3": pmsa.dato3, "id":pmsa.id}
    except:
        respuesta = {}
    return JsonResponse(respuesta)

def json_pmsB(request):
    try:
        pmsa = PMS5003B.objects.last()
        print(pmsa.muestra)
        respuesta = {"pmsA": pmsa.muestra, "dato1": pmsa.dato1,
                    "dato2": pmsa.dato2, "dato3": pmsa.dato3, "id":pmsa.id,
                    "temp": pmsa.temp, "hum":pmsa.hum}
    except:
        respuesta = {}
    return JsonResponse(respuesta)