from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Ciudad(models.Model):
    departamento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=60)

    class Meta:
        ordering = ['nombre']
    def __str__(self):
        return self.nombre

class Dispositivos(models.Model):
    modelo_id = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.modelo_id + self.ubicacion

class Espectro(models.Model):
    espectro_IQ = JSONField(encoder="")
    dispositivo = models.ForeignKey(Dispositivos, on_delete=models.CASCADE)
    frec_central = models.FloatField()

    def __str__(self):
        return "Dispositivo "+str(self.dispositivo)

class UsuariosPrimarios(models.Model):
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    frecuencia = models.FloatField() # MHz
    nombre_emisora = models.CharField(max_length=100)
    clase_emisora = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_emisora + str(self.frecuencia) + " MHz"

