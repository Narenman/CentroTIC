from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Lecturas

#Create your views here. grafica dinamica
@csrf_exempt
def datos_json_pulso(request):
    var = Lecturas.objects.last()
    respuesta = {"datos": [var.fecha, var.hr, var.spo2, var.estado_bateria]}
    print(respuesta)
    return JsonResponse(respuesta)


    
@csrf_exempt
def datos_json_all(request):
    var = Lecturas.objects.all()
    datos = var.values("fecha", "hr","spo2","estado_bateria")
    datos = list(map(lambda datos: [datos["fecha"], datos["hr"], datos["spo2"],datos["estado_bateria"]], datos))
    respuesta = {"datos": datos}
    return JsonResponse(respuesta)
