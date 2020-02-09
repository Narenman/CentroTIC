from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from django.http import Http404

from .serializers import EspectroSerializer
from .models import Espectro

class EspectroAPI(APIView):
    """
    API para actualizar el valor del espectro
    """
    # authentication_classes = ()
    # permission_classes = ()

    def get_object(self, pk):
        try:
            return Espectro.objects.get(pk=pk)
        except Espectro.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        espectro = self.get_object(pk)
        respuesta = {"frecuencia central": espectro.frec_central,
                     "samp_rate": espectro.samp_rate}
        return Response(respuesta)

    def delete(self, request, pk, format=None):
        espectro = self.get_object(pk)
        espectro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        espectro = self.get_object(pk)
        serializer = EspectroSerializer(espectro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)