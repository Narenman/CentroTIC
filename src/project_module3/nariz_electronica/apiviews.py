from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import Http404
from rest_framework import status


from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Lecturas, DatosEvaluar
from .serializers import LecturasSerializer, DatosEvaluarSerializer
import pandas as pd

## Variables ambientales 
class LecturasAPI(generics.CreateAPIView):
      """ Esta API es para almacenar los datos de la nariz
      mediante bloques
      """
      queryset = Lecturas.objects.all()
      serializer_class = LecturasSerializer


class DatosEvaluarAPI(APIView):
    """
    Lista el ultimo valor sensado por la nariz electronica version 1.
    """
    authentication_classes = ()
    permission_classes = ()
    def get(self, request, format=None):
        snippets = DatosEvaluar.objects.last()
        serializer = DatosEvaluarSerializer(snippets, many=False)
        datos = serializer.data
        #retorna los datos por sensores para poder graficarlos
        lista_sensores = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"]
        datos = pd.DataFrame(data=datos["medicion"], columns=lista_sensores)
        respuesta = {"S1":datos["S1"], "S2":datos["S2"], "S3":datos["S3"], "S4":datos["S4"],
                     "S5":datos["S5"], "S6":datos["S6"], "S7":datos["S7"], "S8":datos["S8"],
                     "S9":datos["S9"], "S10":datos["S10"],"S11":datos["S11"],"S12":datos["S12"],
                     "S13":datos["S13"], "S14":datos["S14"],"S15":datos["S15"], "S16":datos["S16"]}
        return Response(respuesta)

    def post(self, request, format=None):
        serializer = DatosEvaluarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)