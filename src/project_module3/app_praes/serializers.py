
from .models import Temperatura, Humedad, PresionAtmosferica, KitNariz, PH_agua, Temperatura_agua, Turbidez_agua, Flujo_agua,\
    Kit
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class KitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = "__all__"

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

#sensores agua
class PHaguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PH_agua
        fields = "__all__"

class TemperaturaAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperatura_agua
        fields = "__all__"

class TurbidezaguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turbidez_agua
        fields = "__all__"

class FlujoaguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flujo_agua
        fields = "__all__"

