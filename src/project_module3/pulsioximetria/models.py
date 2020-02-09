from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Lecturas(models.Model):
    hr = JSONField(encoder="")
    spo2 = JSONField(encoder="")
    estado_bateria = models.FloatField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Lecturas'
        verbose_name_plural = 'Lecturass'