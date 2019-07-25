from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Temperatura, Humedad, PresionAtmosferica, KitNariz,\
    PH_agua, Temperatura_agua, Turbidez_agua,Flujo_agua, Kit
from .serializers import TemperaturaSerializer, HumedadSerializer, PresionAtmosfericaSerializer,\
      UserSerializer, KitNarizSerializer, PHaguaSerializer, TemperaturaAguaSerializer,\
          TurbidezaguaSerializer, FlujoaguaSerializer, KitSerializer
import pandas as pd


class KITAPI(generics.ListCreateAPIView):
    """Se encarga de registrar cada KIT dado a los colegios """
    queryset = Kit.objects.all()
    serializer_class = KitSerializer

class LoginView(APIView):
    """ Esta API es para ver los usuarios registrados hasta el momento
    en la aplicacion del CENTROTIC
    """
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request,):
        users = User.objects.all()
        usuarios = users.values("username", "email")
        return Response(usuarios)

class CrearUsuarioAPI(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserSerializer

# ### calidad del aire Nariz electronica
# class KitNarizAPI(APIView):
#     """ La calidad del aire se evaluara como nariz electronica.
#     """
#     authentication_classes = ()
#     permission_classes = ()
#     # def get(self, request, format=None):
#     #     """ Para mostrar los datos y graficarlos en el navegador """
#     #     #consulta del ultimo dato medido para extraer su asociacion
#     #     snippets = KitNariz.objects.last()
#     #     ultima_asociacion = snippets.asociacion.pk
#     #     # se filta por la asociacion del ultimo dato medido  
#     #     snippets = KitNariz.objects.filter(asociacion=ultima_asociacion)
#     #     serializer = KitNarizSerializer(snippets, many=True)
#     #     datos = serializer.data
#     #     #se realiza una organizacion de los datos para poder retornar la informacion por cada sensor
#     #     med = []
#     #     for dat in datos:
#     #         med.append(dat["medicion"])
#     #     lista_sensores = ["S1","S2","S3","S4",]
#     #     datos = pd.DataFrame(data=med, columns=lista_sensores)
#     #     respuesta = {"S1":datos["S1"], "S2":datos["S2"], "S3":datos["S3"], "S4":datos["S4"],}
#     #     return Response(respuesta)

#     def post(self, request, format=None):
#         serializer = KitNarizSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## Variables ambientales 
class TemperaturaAPI(generics.CreateAPIView):
    """Se encarga de registrar la temperatura con el
    sensor BME280 """
    queryset = Temperatura.objects.all()
    serializer_class = TemperaturaSerializer

class HumedadAPI(generics.CreateAPIView):
    """Se encarga de registrar la humedad relativa con el sensor
    BME280 """
    queryset = Humedad.objects.all()
    serializer_class = HumedadSerializer

class PresionAtmosfericaAPI(generics.CreateAPIView):
    """Se encarga de registrar la presion atmosferica con el 
    sensor BME280 """
    queryset = PresionAtmosferica.objects.all()
    serializer_class = PresionAtmosfericaSerializer

#calidad del aire
class CalidadAireAPI(generics.CreateAPIView):
    """ Se encarga de registar los  valores provenientes 
    de los 10 sensores quimicos para el aire"""
    queryset = KitNariz.objects.all()
    serializer_class = KitNarizSerializer

#Variables agua
class PHAPI(generics.CreateAPIView):
    """Se encarga de registrar el PH del
    agua mediante una sonda que se pone a flotar """
    queryset = PH_agua.objects.all()
    serializer_class = PHaguaSerializer

class TemperaturaAguaAPI(generics.CreateAPIView):
    """Registra la temperatura del agua mediante 
    una sonda que se sumerge en el agua """
    queryset = Temperatura_agua.objects.all()
    serializer_class = TemperaturaAguaSerializer

class TurbidezAguaAPI(generics.CreateAPIView):
    """Registra la turbidez del agua  """
    queryset = Turbidez_agua.objects.all()
    serializer_class = TurbidezaguaSerializer

class FlujoAguaAPI(generics.CreateAPIView):
    """Ayuda a calcular el consumo de agua
    midiendo el flujo que pasa por una tuberia """
    queryset = Flujo_agua.objects.all()
    serializer_class = FlujoaguaSerializer


