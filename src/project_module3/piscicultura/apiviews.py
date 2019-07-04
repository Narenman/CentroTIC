from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from .models import Temperatura, TemperaturaCaja, HumedadCaja, PH, VoltajeBateria, O2disuelto, Pozo
from .serializers import TemperaturaSerializer, TemperaturaCajaSerializer, HumedadCajaSerializer, PHSerializer, O2disueltoSerializer, VoltajeBateriaSerializer, PozoSerializer


class TemperaturaAPIPiscicultura(generics.CreateAPIView):
    """Esta API permite establecer comunicacion entre la raspberry y la base de datos a traves de HTTP """
    queryset = Temperatura.objects.all()
    serializer_class = TemperaturaSerializer

class TemperaturaAPICaja(generics.CreateAPIView):
    """ Esta API permite establecer comunicacion entre la raspberry y la base de datos a traves de HTTP """
    queryset = TemperaturaCaja.objects.all()
    serializer_class = TemperaturaCajaSerializer

class HumedadAPICaja(generics.CreateAPIView):
    """ Esta API permite establecer comunicacion entre la raspberry y la base de datos a traves de HTTP """
    queryset = HumedadCaja.objects.all()
    serializer_class = HumedadCajaSerializer

class PhAPIPiscicultura(generics.CreateAPIView):
    """ Esta API permite establecer comunicacion entre la raspberry y la base de datos a traves de HTTP"""
    queryset = PH.objects.all()
    serializer_class = PHSerializer

class O2DisueltoAPI(generics.CreateAPIView):
    """ Esta API permite establecer comunicacion entre la raspberry y la base de datos a traves de HTTP"""
    queryset = O2disuelto.objects.all()
    serializer_class = O2disueltoSerializer

class VoltajeBateriaAPI(generics.CreateAPIView):
    """ Esta API permite establecer comunicacion entre la raspberry y la base de datos a traves de HTTP"""
    queryset = VoltajeBateria.objects.all()
    serializer_class = VoltajeBateriaSerializer

class PozoAPI(generics.ListCreateAPIView):
    queryset = Pozo.objects.all()
    serializer_class = PozoSerializer
