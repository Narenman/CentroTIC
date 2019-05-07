from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Departamento(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Geolocation(models.Model):
    dane_code= models.IntegerField(primary_key=True)    
    city = models.CharField(max_length=100)
    region = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Geolocation")
        verbose_name_plural = ("Geolocations")

    def __str__(self):
        return self.city


class FrequencyRange(models.Model):
    """
    Provee informacion adicional que puede ayudar a determinal la disponibilidad del espectro,
    provee las frecuencias en las que el dispositivo puede operar
    """
    start_Hz = models.FloatField()
    stop_Hz = models.FloatField()

    def __str__(self):
        return str(self.start_Hz)+" - "+ str(self.stop_Hz)+" Hz"


class DeviceDescriptor(models.Model):
    """
    Contiene parametros para identificar el dispositivo especifico

    """
    serial_Number = models.CharField(max_length=25)
    manufacturer_Id = models.CharField(max_length=25)
    model_Id = models.CharField(max_length=25)
    ruleset_Ids = JSONField()
    device_capabilities = models.ForeignKey(FrequencyRange, on_delete=models.CASCADE)
    geolocation = models.ForeignKey(Geolocation, on_delete=models.CASCADE)

    def __str__(self):
        return self.serial_Number

class DeviceOwner(models.Model):
    """
    Provee informacion de los propietarios
    """
    company = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    device_descriptor = models.ForeignKey(DeviceDescriptor, on_delete=models.CASCADE)

class RulsetInfo(models.Model):
    """
    Contiene las reglas de dominio del ente regulador
    """
    authority = models.CharField(max_length=50)
    rulsetId = models.CharField(max_length=50)


class EventTime(models.Model):
    """ Indica el periodo de tiempo sobre el cual el espectro
    es valido
    """
    start_Time = models.DateTimeField(auto_now=False, auto_now_add=False)
    stop_Time = models.DateTimeField(auto_now=False, auto_now_add=False)

class Spectrum(models.Model):
    operation = models.CharField(max_length=50)
    channels = models.IntegerField()
    geolocation = models.ForeignKey(Geolocation, on_delete=models.CASCADE)

class SpectrumSchedule(models.Model):
    """Indica el periodo de tiempo sobre el cual ese espectro esta disponible
    """
    eventTime = models.ForeignKey(EventTime, on_delete=models.CASCADE)
    spectrum = models.ForeignKey(Spectrum, on_delete=models.CASCADE)

class SpectrumSpec(models.Model):
    """Muestra la disponibilidad de espectro para un conjunto de reglas
    """
    rulset_Info = models.ForeignKey(RulsetInfo, on_delete=models.CASCADE)
    spectrum_Schedules = models.ForeignKey(SpectrumSchedule, on_delete=models.CASCADE)
    time_Range = models.ForeignKey(EventTime, on_delete=models.CASCADE)
    frequency_Ranges = JSONField(encoder="")
    needs_Spectrum_Report = models.BooleanField()
    max_Total_BwHz = models.FloatField(blank=True)
    max_Contiguous_Bw_Hz = models.FloatField(blank=True)
    geolocation = models.ForeignKey(Geolocation, on_delete=models.CASCADE)

class DeviceValidity(models.Model):
    deviceDesc = models.ForeignKey(DeviceDescriptor, on_delete=models.CASCADE)
    isValid = models.BooleanField()
    reason = models.CharField(max_length=150)