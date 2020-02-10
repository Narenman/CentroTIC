from django.shortcuts import render
#import paho.mqtt.client as mqttClient
from django.http import JsonResponse
from .models import SENSORES4

# Create your views here.

def index(request):
    return render(request, "nariz_electronicaV2/index.html",{})

def json_mq(request):
	try:
		mq1 = SENSORES4.objects.all()
		mq1 = mq1.values( "s1", "s2", "s3","s4", "id")
		mq1 = list(map(lambda datos: [ datos["s1"], datos["s2"],datos["s3"],datos["s4"],datos["id"]], mq1))
		respuesta = {"mq": mq1}
	except:
		respuesta = {}
	return JsonResponse(respuesta)
