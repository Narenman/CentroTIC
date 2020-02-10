from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import permissions

from .models import SENSORES4
from .serializers import SENSORES4Serializer
 
class SENSORES4API(generics.ListCreateAPIView):
    """Se encarga de registrar los valores de 
    la tabla donde se hace la lectura de los 4 sensores"""
    queryset = SENSORES4.objects.all()
    serializer_class = SENSORES4Serializer

