from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import AlbumImagenes, Espectro, EstacionAmbiental, CaracteristicasEspectro
from .serializers import AlbumSerializer, EstacionAmbientalSerializer, EspectroSerializer

class AlbumAPI(generics.CreateAPIView):
    """ Esta API se encarga de las imagenes recolectadas por la camara startlight 
    """
    queryset = AlbumImagenes.objects.all()
    serializer_class = AlbumSerializer

class EspectroAPI(APIView):
    """ Esta API se encarga de gestiornar el espectro para poder almacenarlo
    correctamente
    """
    def get(self, request, format=None):
        espectro = Espectro.objects.last()
        serializer = EspectroSerializer(espectro, many=False)
        datos = serializer.data
        return Response(datos)

    def post(self, request, format=None):
        serializer = EspectroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)