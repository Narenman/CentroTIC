from django.db import models
from django.contrib.postgres.fields import JSONField


# region de medicion
class RegionCampana(models.Model):
    """ esta tabla registra tres zonas de medicion, desierto tatacoa, paramo berlin y nevado del cocuy """
    zona = models.CharField(max_length=100)
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)

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
    s_x = JSONField(encoder="")
    area_efec = JSONField(encoder="")
    directividad_antena = JSONField(encoder="")
    referencia = models.CharField(max_length=50)
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
    intensidad_luz = models.FloatField()
    luz_uv = models.FloatField()
    region = models.ForeignKey(RegionCampana, on_delete=models.CASCADE)

    def __str__(self):
        return "Temperatura {}".format(self.temperatura)

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

    class Meta:
        db_table = ''
        managed = True
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return "estado: "+ str(self.activo)

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