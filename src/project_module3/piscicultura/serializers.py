
from rest_framework import serializers
from .models import Temperatura, TemperaturaCaja, HumedadCaja, PH, O2disuelto, VoltajeBateria, Pozo

class TemperaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperatura
        fields = "__all__"


class TemperaturaCajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturaCaja
        fields = "__all__"

class HumedadCajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumedadCaja
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
