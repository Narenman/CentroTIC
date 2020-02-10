from rest_framework import serializers
from .models import SENSORES4

class SENSORES4Serializer(serializers.ModelSerializer):
    class Meta:
        model = SENSORES4
        fields = "__all__"

