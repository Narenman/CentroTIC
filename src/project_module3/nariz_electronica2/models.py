from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class SENSORES4(models.Model):
    #muestra = models.CharField(max_length=100)
    s1 = models.FloatField()
    s2 = models.FloatField()
    s3 = models.FloatField()
    s4 = models.FloatField()


    #s1 = JSONField(encoder="")
    #s2 = JSONField(encoder="")
    #s3 = JSONField(encoder="")
    #s4 = JSONField(encoder="")


    def __str__(self):
    	return str(self.s1)

    #    return self.muestra

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'SENSORES4'
        verbose_name_plural = 'SENSORES4s'
        

