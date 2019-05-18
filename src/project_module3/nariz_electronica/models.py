from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Entrenamiento(models.Model):
    """Este modelo se encarga de administrar los entrenamientos,
    por ejemplo: si se desea entrenar la nariz para lecturas del
    mal de chagas todos los analisis se asociaran al entrenamiento dado
    """
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Analisis(models.Model):
    """ Este modelo se encarga de administrar las diferentes mediciones
    asociadas a un experimento, por ejemplo, alejar la muestra 10 cm, 20 cm, etc...
    """
    nombre = models.CharField(max_length=150)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)
    tiempo_medicion_segundos = models.FloatField()
    
    def __str__(self): 
        return str(self.pk)

class Lecturas(models.Model):
    """ Este modelo almacena los datos recolectados por experimento
    en la base de datos"""
    medicion = JSONField(encoder="")
    analisis = models.ForeignKey(Analisis, on_delete=models.CASCADE)
    
