from django.contrib import admin
from .models import Pozo, Temperatura, TemperaturaCaja, O2disuelto, PH, HumedadCaja, TomaDatos, VoltajeBateria
# Register your models here.
admin.site.register(Pozo)
admin.site.register(Temperatura)
admin.site.register(TemperaturaCaja)
admin.site.register(O2disuelto)
admin.site.register(PH)
admin.site.register(HumedadCaja)
admin.site.register(TomaDatos)
admin.site.register(VoltajeBateria)

