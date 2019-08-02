from django.db import models

# Create your models here.
class PMS5003A(models.Model):
    muestra = models.CharField(max_length=100)
    dato1 = models.FloatField()
    dato2 = models.FloatField()
    dato3 = models.FloatField()

    def __str__(self):
        return self.muestra

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PMS5003A'
        verbose_name_plural = 'PMS5003As'

class PMS5003B(models.Model):
    muestra = models.CharField(max_length=100)
    dato1 = models.FloatField()
    dato2 = models.FloatField()
    dato3 = models.FloatField()
    temp = models.FloatField()
    hum = models.FloatField()
    
    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PMS5003B'
        verbose_name_plural = 'PMS5003Bs'   
        