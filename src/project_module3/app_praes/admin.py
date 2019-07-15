from django.contrib import admin
from .models import Departamento, Ciudad, Kit, Colegio, Sensores, Semillero, Temperatura, \
    Humedad, PresionAtmosferica, Asociacion, KitNariz, Temperatura_agua, PH_agua, Turbidez_agua, Flujo_agua
# Register your models here.

admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Kit)
admin.site.register(Colegio)
admin.site.register(Semillero)
admin.site.register(Sensores)

#variables
admin.site.register(Temperatura)
admin.site.register(Humedad)
admin.site.register(PresionAtmosferica)
admin.site.register(PH_agua)
admin.site.register(Temperatura_agua)
admin.site.register(Turbidez_agua)
admin.site.register(Flujo_agua)



#modo nariz
admin.site.register(Asociacion)
admin.site.register(KitNariz)






