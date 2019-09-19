from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from .models import AlbumImagenes, Espectro, EstacionAmbiental, CaracteristicasEspectro, Estado ,\
    PosicionAntena
from .serializers import AlbumSerializer, EstacionAmbientalSerializer, EspectroSerializer ,\
    CaractEspectroSerializer, EstadoSerializer, PosicionAntenaSerializer

class AlbumAPI(generics.CreateAPIView):
    """ Esta API se encarga de las imagenes recolectadas por la camara startlight 
    """
    authentication_classes = ()
    permission_classes = ()

    queryset = AlbumImagenes.objects.all()
    serializer_class = AlbumSerializer

class EspectroAPI(APIView):
    """ Esta API se encarga de gestiornar el espectro para poder almacenarlo
    correctamente
    """
    # authentication_classes = ()
    # permission_classes = ()
    def get(self, request, format=None):
        espectro = Espectro.objects.last()
        serializer = EspectroSerializer(espectro, many=False)
        datos = serializer.data
        return Response({"frec_central": datos["frec_central"],
                         "frec_muestreo": datos["frec_muestreo"],
                         "id": datos["id"]})

    def post(self, request, format=None):
        serializer = EspectroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CaracteristicasEspectroAPI(generics.CreateAPIView):
    """Esta API se encarga de registrar las caracteristicas del espectro
    sensado """
    # authentication_classes = ()
    # permission_classes = ()
    
    queryset = CaracteristicasEspectro.objects.all()
    serializer_class = CaractEspectroSerializer

class EstacionAmbientalAPI(generics.CreateAPIView):
    queryset = EstacionAmbiental.objects.all()
    serializer_class = EstacionAmbientalSerializer

class EstadoAPI(APIView):
    """Esta API se encarga de monitorear el estado 
    del sistema RFI, es decir, si esta activo o 
    inactivo """
    authetication_classes = ()
    permission_classes = ()

    def get_object(self, pk):
        try:
            return Estado.objects.get(pk=pk)
        except Estado.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        estado = self.get_object(pk=pk)
        print(estado)
        respuesta = {"activo": estado.activo,
                    "frecuencia": estado.frecuencia,
                    "azimut": estado.azimut,
                    "elevacion":estado.elevacion}
        return Response(respuesta)

    def put(self, request, pk, format=None):
        estado = self.get_object(pk=pk)
        serializer = EstadoSerializer(estado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PosicionAntenaAPI(APIView):
    def post(self, request, format=None):
        serializer = PosicionAntenaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)