from django.contrib import admin
from .models import Ciudad, Kit, Colegio, Semillero, Temperatura, \
    Humedad, PresionAtmosferica, KitNariz, Temperatura_agua, PH_agua, Turbidez_agua, \
         Flujo_agua, Ubicacion_lectura
# Register your models here.

# admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Kit)
admin.site.register(Colegio)
admin.site.register(Semillero)

#variables
admin.site.register(Temperatura)
admin.site.register(Humedad)
admin.site.register(PresionAtmosferica)
admin.site.register(PH_agua)
admin.site.register(Temperatura_agua)
admin.site.register(Turbidez_agua)
admin.site.register(Flujo_agua)
admin.site.register(Ubicacion_lectura)

#modo nariz
admin.site.register(KitNariz)






