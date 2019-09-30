from django.db import models
from django.contrib.postgres.fields import JSONField


# region de medicion
class RegionCampana(models.Model):
    """ esta tabla registra tres zonas de medicion, desierto tatacoa, paramo berlin y nevado del cocuy """
    zona = models.CharField(max_length=100)
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    latitud = models.CharField(max_length=50, blank=True)
    longitud = models.CharField(max_length=50, blank=True)
    imagen = models.ImageField(upload_to="album/regiones", height_field=None, width_field=None, max_length=None, blank=True)

    def __str__(self):
        return self.zona

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'RegionCampana'
        verbose_name_plural = 'RegionCampanas'

# subsistema RFI
class Espectro(models.Model):
    """ esta tabla registra el espectro medido por el sistema """
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    espectro = JSONField(encoder="")
    frec_muestreo = models.IntegerField()
    nfft = models.IntegerField()
    frec_central = models.FloatField()
    duracion = models.FloatField()
    region = models.ForeignKey(RegionCampana, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.frec_central)+" RBW "+str(float(self.frec_muestreo)/float(self.nfft))


class CaracteristicasEspectro(models.Model):
    """ esta tabla registra caracteristicas adicionales de las mediciones del espectro, puede ser util para 
    el procesamiento"""
    max_v = JSONField(encoder="")
    min_v = JSONField(encoder="")
    energia = JSONField(encoder="")
    espectro = models.ForeignKey(Espectro, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.energia)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'CaracteristicasEspectro'
        verbose_name_plural = 'CaracteristicasEspectros'

class CaracteristicasAntena(models.Model):
    """ esta tabla registra los parametros relacionados con la antena """
    referencia = models.CharField(max_length=50)
    rango_frecuencias = models.CharField(max_length=50)
    polarizacion = models.CharField(max_length=50, blank=True)
    vswr = models.ImageField(upload_to="album/vswr", height_field=None, width_field=None, max_length=None)
    conector = models.CharField(max_length=50, blank=True)
    directividad = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="album/antenas", height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.referencia

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'CaracteristicasAntena'
        verbose_name_plural = 'CaracteristicasAntenas'

# subsistema posicionamiento
class PosicionAntena(models.Model):
    """ esta tabla registra las posiciones de la antena en angulos azimut
    y elevacion"""
    azimut  = models.FloatField()
    elevacion = models.FloatField()
    antena = models.ForeignKey(CaracteristicasAntena, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    region = models.ForeignKey(RegionCampana, on_delete=models.CASCADE)

    def __str__(self):
        return "azimut {} elevacion {}".format(self.azimut, self.elevacion)

# subsistema de estacion de monitoreo
class EstacionAmbiental(models.Model):
    """ esta tabla registra variables ambientales """
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    temperatura = models.FloatField()
    humedad_relativa = models.FloatField()
    presion_atomosferica = models.FloatField()
    radiacion_solar = models.FloatField()
    vel_viento = models.FloatField()
    dir_viento = models.CharField( max_length=50)
    precipitacion = models.FloatField()

    region = models.ForeignKey(RegionCampana, on_delete=models.CASCADE)

    def __str__(self):
        return "Temperatura {} humedad {}".format(self.temperatura, self.humedad_relativa)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'EstacionAmbiental'
        verbose_name_plural = 'EstacionAmbientals'

class CaracteristicasEstacion(models.Model):
    """ esta tabla registra la informacion de los sensores de la estacion terrena"""
    sensor = models.CharField(max_length=50)
    variable = models.CharField(max_length=50)
    rango = models.CharField(max_length=50)
    resolucion = models.CharField(max_length=50)

    def __str__(self):
        return self.sensor

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'CaracteristicasEstacion'
        verbose_name_plural = 'CaracteristicasEstacions'


# subsistema recoleccion de imagenes del cielo

class AlbumImagenes(models.Model):
    """ esta tabla se encarga de registrar todas las imagenes del cielo tomadas """
    # imagen = models.ImageField(upload_to='album/imagenes', height_field=None, width_field=None, max_length=None)
    imagen = models.FileField(upload_to='videos/', null = True, max_length=200, verbose_name="")
    fecha = models.DateTimeField(auto_now_add=True, auto_now=False)
    region = models.ForeignKey(RegionCampana, on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.imagen)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'AlbumImagenes'
        verbose_name_plural = 'AlbumImageness'


class Estado(models.Model):
    activo = models.BooleanField(default=False)
    frecuencia = models.FloatField()
    azimut = models.FloatField()
    elevacion = models.FloatField()
  
    class Meta:
        db_table = ''
        managed = True
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return "estado: "+ str(self.activo)

class Estadocamara(models.Model):
    camara = models.BooleanField(default=False)
    def __str__(self):
        return "estado: "+ str(self.camara)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Estadocamara'
        verbose_name_plural = 'Estadocamaras'

class Estadoestacion(models.Model):
    estacion = models.BooleanField(default=False)
    def __str__(self):
        return "estado: "+str(self.estacion)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Estadoestacion'
        verbose_name_plural = 'Estadoestacions'

class RBW(models.Model):
    frecuencia_muestreo = models.IntegerField()
    nfft = models.IntegerField()
    rbw = models.FloatField()

    def __str__(self):
        return "RBW {}".format(str(self.rbw))

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'RBW'
        verbose_name_plural = 'RBWs'
        ordering = ["rbw"]

class Bandas(models.Model):
    banda = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)
    frecuencia_inicial = models.FloatField()
    frecuencia_final = models.FloatField()

    def __str__(self):
        return self.abreviatura

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Bandas'
        verbose_name_plural = 'Bandass'

class Servicios(models.Model):
    servicio = models.CharField(max_length=200)
    frecuencia_inicial = models.FloatField()
    frecuencia_final = models.FloatField()
    banda = models.ForeignKey(Bandas, on_delete=models.CASCADE)

    def __str__(self):
        return self.servicio

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Servicios'
        verbose_name_plural = 'Servicioss'