from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Lecturas
from .serializers import LecturasSerializer

## Variables ambientales 
class LecturasAPI(generics.CreateAPIView):
      """ Esta API es para almacenar los datos de la nariz
      mediante bloques
      """
      queryset = Lecturas.objects.all()
      serializer_class = LecturasSerializer