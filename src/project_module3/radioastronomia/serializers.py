from rest_framework import serializers

from .models import AlbumImagenes, Espectro, EstacionAmbiental, CaracteristicasEspectro ,\
    Estado, PosicionAntena, Estadocamara, Estadoestacion, EstadoPosicionAntena


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

class EstadoCamaraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadocamara
        fields = "__all__"

class EstadoEstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadoestacion
        fields = "__all__"

class PosicionAntenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicionAntena
        fields = "__all__"

class EstadoPosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPosicionAntena
        fields = "__all__"