from django.db import models

# Create your models here.
class Pozo(models.Model):
    """Contiene informacion basica del pozo donde se cultivan los pescados"""
    nombre = models.CharField(max_length=50)
    area = models.FloatField() # m^2
    cantidad_peces = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Temperatura(models.Model):
    """ Utilizado para almacena la temperatura del agua donde estan los pescados """
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    pozo = models.ForeignKey(Pozo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.valor)+" °C"

class O2disuelto(models.Model):
    """Se utiliza para almacenar el oxigeno disuelto en el agua donde estan los pescados"""
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    pozo = models.ForeignKey(Pozo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.valor) + "O2 disuelto"

class PH(models.Model):
    """ Mide el PH del agua del pozo donde estan los pescados """
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    pozo = models.ForeignKey(Pozo, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.valor)+" PH"

class TemperaturaAmbiente(models.Model):
    """ Mide la temperatura del ambiente donde se encuentra el kit de monitoreo """
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    pozo = models.ForeignKey(Pozo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.valor)+" Temperatura ambiente"

class VoltajeBateria(models.Model):
    """ Mide el voltaje de la bateria del kit de monitoreo """
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    pozo = models.ForeignKey(Pozo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.valor)+" V"

    

