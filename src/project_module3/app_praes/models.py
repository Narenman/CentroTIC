from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_departamento

class Ciudad(models.Model):
    nombre_ciudad = models.CharField(max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_ciudad
        
class Colegio(models.Model):
    nombre_colegio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50, unique=True)
    nombre_rector = models.CharField(max_length=50)
    correo_rector = models.EmailField(max_length=254)
    direccion_colegio = models.CharField(max_length=50)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_colegio

class Kit(models.Model):
    nombre_kit = models.CharField(max_length=50)
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre_kit

class Ubicacion_lectura(models.Model):
    etiqueta_ubicacion = models.CharField(max_length=100)
    def __str__(self):
        return self.etiqueta_ubicacion
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Ubicacion_lectura'
        verbose_name_plural = 'Ubicacion_lecturas'

class Semillero(models.Model):
    responsable = models.CharField(max_length=50)
    telefono = models.IntegerField()
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE)

    def __str__(self):
        return self.responsable

class Integrantes(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.IntegerField()
    semillero = models.ForeignKey(Semillero, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

#registro de variables
class Temperatura(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    valor = models.FloatField()
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)
    def __str__(self):
        return "temperatura " + str(self.valor)+ " °C"

class Humedad(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    valor = models.FloatField()
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)

    def __str__(self):
        return "humedad " + str(self.valor)+ " %"

class PresionAtmosferica(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    valor = models.FloatField()
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)

    def __str__(self):
        return "presion " + str(self.valor)+ " mbar"

class KitNariz(models.Model):
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    valor = JSONField(encoder="",)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)
    def __str__(self):
        return "modo nariz"+str(self.pk)

#variables del agua
class PH_agua(models.Model):
    valor = models.FloatField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)

    def __str__(self):
        return "valor PH "+str(self.valor)

class Temperatura_agua(models.Model):
    valor = models.FloatField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)

    def __str__(self):
        return "Temperatura agua "+str(self.valor)

class Turbidez_agua(models.Model):
    valor = models.FloatField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)

    def __str__(self):
        return "turbidez agua "+str(self.valor)

class Flujo_agua(models.Model):
    valor = models.FloatField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    kit_monitoreo = models.ForeignKey(Kit, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion_lectura, on_delete=models.CASCADE)

    def __str__(self):
        return "Flujo agua "+str(self.valor)

