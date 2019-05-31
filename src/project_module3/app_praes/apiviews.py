from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Temperatura, Humedad, PresionAtmosferica, MaterialParticulado, NO2, \
      Polvo, O3, SO2, CO, CO2, MetanoPropanoCO, LuzUV, MaterialOrganico, CH4, Anemometro, Sensores, KitNariz
from .serializers import TemperaturaSerializer, HumedadSerializer, PresionAtmosfericaSerializer, \
      MaterialParticuladoSerializer, NO2Serializer, PolvoSerializer, O3Serializer, SO2Serializer, \
      COSerializer, CO2Serializer, MetanoPropanoCOSerializer, LuzUVSerializer,\
      MaterialOrganicoSerializer, CH4Serializer, AnemometroSerializer, UserSerializer, SensoresSerializer, KitNarizSerializer
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
    """
    Lista el ultimo valor sensado por el kit praes en modo nariz.
    """
    authentication_classes = ()
    permission_classes = ()
    def get(self, request, format=None):
        snippets = KitNariz.objects.last()
        serializer = KitNarizSerializer(snippets, many=False)
        datos = serializer.data
        #retorna los datos por sensores para poder graficarlos
        lista_sensores = ["S1","S2","S3","S4",]
        datos = pd.DataFrame(data=datos["medicion"], columns=lista_sensores)
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

class MaterialParticuladoAPI(generics.CreateAPIView):
    queryset = MaterialParticulado.objects.all()
    serializer_class = MaterialParticuladoSerializer

class NO2API(generics.CreateAPIView):
    queryset = NO2.objects.all()
    serializer_class = NO2Serializer

class PolvoAPI(generics.CreateAPIView):
    queryset = Polvo.objects.all()
    serializer_class = PolvoSerializer

class O3API(generics.CreateAPIView):
    queryset = O3.objects.all()
    serializer_class = O3Serializer

class SO2API(generics.CreateAPIView):
    queryset = SO2.objects.all()
    serializer_class = SO2Serializer

class COAPI(generics.CreateAPIView):
    queryset = CO.objects.all()
    serializer_class = COSerializer

class CO2API(generics.CreateAPIView):
    queryset = CO2.objects.all()
    serializer_class = CO2Serializer

class MetanoPropanoCOAPI(generics.CreateAPIView):
    queryset = MetanoPropanoCO.objects.all()
    serializer_class = MetanoPropanoCOSerializer

class LuzUVAPI(generics.CreateAPIView):
    queryset = LuzUV.objects.all()
    serializer_class = LuzUVSerializer

class MaterialOrganicoAPI(generics.CreateAPIView):
    queryset = MaterialOrganico.objects.all()
    serializer_class = MaterialOrganicoSerializer

class CH4API(generics.CreateAPIView):
    queryset = CH4.objects.all()
    serializer_class = CH4Serializer

class AnemometroAPI(generics.CreateAPIView):
    queryset = Anemometro.objects.all()
    serializer_class = AnemometroSerializer