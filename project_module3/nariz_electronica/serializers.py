from .models import Entrenamiento, Analisis, Lecturas
from rest_framework import serializers

class LecturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturas
        fields = "__all__"
