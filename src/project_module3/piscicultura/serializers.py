
from rest_framework import serializers
from .models import Temperatura, TemperaturaAmbiente, PH, O2disuelto, VoltajeBateria, Pozo

class TemperaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperatura
        fields = "__all__"


class TemperaturaAmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturaAmbiente
        fields = "__all__"


class PHSerializer(serializers.ModelSerializer):
    class Meta:
        model = PH
        fields = "__all__"


class O2disueltoSerializer(serializers.ModelSerializer):
    class Meta:
        model = O2disuelto
        fields = "__all__"


class VoltajeBateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoltajeBateria
        fields = "__all__"

class PozoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pozo
        fields = "__all__"