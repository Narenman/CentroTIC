from rest_framework import generics 
from rest_framework import status

from pulsioximetria import serializers
from pulsioximetria import models

class LecturasAPI(generics.ListCreateAPIView):
    """Se encarga de registrar cada KIT dado a los colegios """
    queryset = models.Lecturas.objects.all()
    serializer_class = serializers.LecturasSerializer