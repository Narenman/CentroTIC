from django.contrib import admin
from piscicultura import models

# Register your models here.
admin.site.register(models.Temperatura)
admin.site.register(models.O2disuelto)
admin.site.register(models.PH)
admin.site.register(models.TemperaturaCaja)
admin.site.register(models.HumedadCaja)
admin.site.register(models.VoltajeBateria)





