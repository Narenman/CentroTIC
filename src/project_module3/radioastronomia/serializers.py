from rest_framework import serializers

from .models import AlbumImagenes, Espectro, EstacionAmbiental


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