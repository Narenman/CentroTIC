from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import permissions

from .models import PMS5003A, PMS5003B
from .serializers import PMS5003ASerializer, PMS5003BSerializer
 
class Pms5003aAPI(generics.ListCreateAPIView):
    """Se encarga de registrar los valores de 
    la tabla del sensor 1"""
    queryset = PMS5003A.objects.all()
    serializer_class = PMS5003ASerializer

class Pms5003bAPI(generics.ListCreateAPIView):
    """Se encarga de registrar los valores de 
    la tabla del sensor 2"""
    queryset = PMS5003B.objects.all()
    serializer_class = PMS5003BSerializer