from rest_framework import serializers

from .models import AlbumImagenes, Espectro, EstacionAmbiental, CaracteristicasEspectro ,\
    Estado


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImagenes
        fields = "__all__"

class EspectroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espectro
        fields = "__all__"

class EstacionAmbientalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstacionAmbiental
        fields = "__all__" 

class CaractEspectroSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicasEspectro
        fields = "__all__"

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = "__all__"