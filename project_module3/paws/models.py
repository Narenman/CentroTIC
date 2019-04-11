from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Point(models.Model):
    latitude = models.CharField(max_length=25)
    longitude = models.CharField(max_length=25)

class Ellipse(models.Model):
    semi_Major_Axis = models.FloatField()
    semi_Minor_Axis = models.FloatField()
    orientation = models.FloatField()
    center = models.ForeignKey(Point, on_delete=models.CASCADE)


class Geolocation(models.Model):
    """
    Para expresar las coordenadas en unidades de grados y metros
    """
    point = models.ForeignKey(Ellipse, on_delete=models.CASCADE)
    confidence = models.IntegerField(default=95)

    def __str__(self):
        return "Geolocation "+ str(self.confidence)

class AntennaCharacteristics(models.Model):
    """
    AGL: Above Ground Level (default)
    AMSL: Above Mean Sea Level)
    """
    height = models.FloatField()
    AGL = "AGL"
    AMSL = "AMSL"
    enum_heigtType =  ((AGL, "Above Ground Level"), (AMSL, "AMSL: Above Mean Sea Level"))
    height_Type = models.CharField(max_length=50, choices=enum_heigtType, default=AGL)
    antenna_direction = models.CharField(max_length=20, blank=True)
    antenna_radiation_pattern = models.CharField(max_length=15, blank=True)
    antenna_gain = models.FloatField(blank=True)

class FrequencyRange(models.Model):
    """
    Provee informacion adicional que puede ayudar a determinal la disponibilidad del espectro,
    provee las frecuencias en las que el dispositivo puede operar
    """
    start_Hz = models.FloatField()
    stop_Hz = models.FloatField()

    def __str__(self):
        return str(self.start_Hz)+" - "+ str(self.stop_Hz)+" Hz"

# class DeviceCapabilities(models.Model):
#     frequencyRanges = models.ForeignKey(FrequencyRange, on_delete=models.CASCADE)


class DeviceDescriptor(models.Model):
    """
    Contiene parametros para identificar el dispositivo especifico

    """
    serial_Number = models.CharField(max_length=25)
    manufacturer_Id = models.CharField(max_length=25)
    model_Id = models.CharField(max_length=25)
    ruleset_Ids = JSONField()
    anttenna_characteristics = models.ForeignKey(AntennaCharacteristics, on_delete=models.CASCADE)
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
    address = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=50)
    department = models.CharField( max_length=50)
    device_descriptor = models.ForeignKey(DeviceDescriptor, on_delete=models.CASCADE)

class RulsetInfo(models.Model):
    """
    Contiene las reglas de dominio del ente regulador
    """
    authority = models.CharField(max_length=50)
    rulsetId = models.CharField(max_length=50)
    max_Location_Change = models.FloatField(blank=True)
    max_Polling_Secs = models.FloatField(blank=True)


class EventTime(models.Model):
    """ Indica el periodo de tiempo sobre el cual el espectro
    es valido
    """
    start_Time = models.DateTimeField(auto_now=False, auto_now_add=False)
    stop_Time = models.DateTimeField(auto_now=False, auto_now_add=False)

class Spectrum(models.Model):
    resolution_Bw_Hz = models.FloatField()
    profiles = JSONField()
    geolocation = models.ForeignKey(Geolocation, on_delete=models.CASCADE)

class SpectrumProfilePoint(models.Model):
    hz = models.FloatField()
    dbm = models.FloatField()
    
class SpectrumProfile(models.Model):
    """Se caracteriza por una lista ordenada de la potencia maxima permitida
    """
    list1= models.ForeignKey(SpectrumProfilePoint, on_delete=models.CASCADE)
    rulsetinfo = models.ForeignKey(RulsetInfo, on_delete=models.CASCADE)


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