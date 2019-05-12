from django.db import models
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
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_colegio

class Kit(models.Model):
    nombre_kit = models.CharField(max_length=50)
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=200, null=True)
    ubicacion_kit = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_kit

class Sensores(models.Model):
    nombre_sensor = models.CharField(max_length=50)
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.nombre_sensor

class Temperatura(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "temperatura " + str(self.valor)+ " °C"


class Humedad(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "humedad " + str(self.valor)+ " %"

class PresionAtmosferica(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "presion " + str(self.valor)+ " mbar"

class MaterialParticulado(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)

class NO2(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "NO2 {} ppm".format(self.valor)

class Polvo(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "polvo {} mg/cm^2".format(self.valor)

class O3(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "O3 {} ppm".format(self.valor)

class SO2(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "SO2 {} ppm".format(self.valor)
    
class CO(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "CO {} ppm".format(self.valor)

class CO2(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "CO2 {} ppm".format(self.valor)

class MetanoPropanoCO(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)

class LuzUV(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "luz uv {} mW/cm^2".format(self.valor)

class MaterialOrganico(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "material organico {} ppm".format(self.valor)

class CH4(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    def __str__(self):
        return "CH4 {} ppm".format(self.valor)

class Anemometro(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    valor = models.FloatField()
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)

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

