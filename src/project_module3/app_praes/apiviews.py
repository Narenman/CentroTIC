from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Temperatura, Humedad, PresionAtmosferica, Sensores, KitNariz
from .serializers import TemperaturaSerializer, HumedadSerializer, PresionAtmosfericaSerializer,\
      UserSerializer, SensoresSerializer, KitNarizSerializer
import pandas as pd


# class SensoresAPI(APIView):
#     """ Provee la lista de todos los sensores usados para el monitoreo ambiental,
#     esto es util para programar la tarjeta de desarrollo o terminal IoT, 
#     solo el administrador tiene acceso a esta API
#     """
#     permission_classes = (permissions.IsAdminUser,)
#     def get(self, request, format=None):
#         datos = Sensores.objects.all()
#         sensores = datos.values("id", "nombre_sensor")
#         return Response(sensores)

# Clases para el administrador centroTIC

# class LoginView(APIView):
#     permission_classes = (permissions.IsAdminUser,)

#     def post(self, request,):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({"token": user.auth_token.key})
#         else:
#             return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class KitNarizAPI(APIView):
    """ La calidad del aire se evaluara como nariz electronica.
    """
    authentication_classes = ()
    permission_classes = ()
    def get(self, request, format=None):
        """ Para mostrar los datos y graficarlos en el navegador """
        #consulta del ultimo dato medido para extraer su asociacion
        snippets = KitNariz.objects.last()
        ultima_asociacion = snippets.asociacion.pk
        # se filta por la asociacion del ultimo dato medido  
        snippets = KitNariz.objects.filter(asociacion=ultima_asociacion)
        serializer = KitNarizSerializer(snippets, many=True)
        datos = serializer.data
        #se realiza una organizacion de los datos para poder retornar la informacion por cada sensor
        med = []
        for dat in datos:
            med.append(dat["medicion"])
        lista_sensores = ["S1","S2","S3","S4",]
        datos = pd.DataFrame(data=med, columns=lista_sensores)
        respuesta = {"S1":datos["S1"], "S2":datos["S2"], "S3":datos["S3"], "S4":datos["S4"],}
        return Response(respuesta)

    def post(self, request, format=None):
        serializer = KitNarizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """ Esta API es para ver los usuarios registrados hasta el momento
    en la aplicacion del CENTROTIC
    """
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request,):
        users = User.objects.all()
        usuarios = users.values("username", "email")
        return Response(usuarios)

class SensoresAPI(generics.ListCreateAPIView):
    """ Provee la lista de todos los sensores usados para el monitoreo ambiental,
    esto es util para programar la tarjeta de desarrollo o terminal IoT, 
    solo el administrador tiene acceso a esta API
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer

class CrearUsuarioAPI(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserSerializer
###

## Variables ambientales 
class TemperaturaAPI(generics.CreateAPIView):
    queryset = Temperatura.objects.all()
    serializer_class = TemperaturaSerializer

class HumedadAPI(generics.CreateAPIView):
    queryset = Humedad.objects.all()
    serializer_class = HumedadSerializer

class PresionAtmosfericaAPI(generics.CreateAPIView):
    queryset = PresionAtmosferica.objects.all()
    serializer_class = PresionAtmosfericaSerializer





