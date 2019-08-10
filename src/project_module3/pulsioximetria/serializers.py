from rest_framework import serializers
from .models import Lecturas

class LecturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturas
        fields = "__all__"