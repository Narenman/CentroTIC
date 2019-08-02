from rest_framework import serializers
from .models import PMS5003A, PMS5003B

class PMS5003ASerializer(serializers.ModelSerializer):
    class Meta:
        model = PMS5003A
        fields = "__all__"

class PMS5003BSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMS5003B
        fields = "__all__"