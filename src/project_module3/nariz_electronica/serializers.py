from .models import Entrenamiento, Analisis, Lecturas, DatosEvaluar
from rest_framework import serializers

class LecturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturas
        fields = "__all__"

class DatosEvaluarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosEvaluar
        fields = "__all__"