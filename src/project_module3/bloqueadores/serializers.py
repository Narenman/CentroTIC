from rest_framework import serializers
from .models import Espectro

class EspectroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espectro
        fields = "__all__"