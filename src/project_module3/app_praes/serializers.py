
from .models import Temperatura, Humedad, PresionAtmosferica, Sensores, KitNariz
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class KitNarizSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitNariz
        fields = "__all__"

class TemperaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperatura
        fields = "__all__"

class HumedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Humedad
        fields = "__all__"

class PresionAtmosfericaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresionAtmosferica
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class SensoresSerializer(serializers.ModelSerializer):
    """
    Lista de sensores que se encuentran en la API para monitorear el ambiente
    """
    class Meta:
        model = Sensores
        fields ="__all__"