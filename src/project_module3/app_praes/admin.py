from django.contrib import admin
from .models import Departamento, Ciudad, Kit, Colegio, Sensores, Semillero, Temperatura, \
    Humedad, PresionAtmosferica, MaterialParticulado, NO2, \
    Polvo, O3, SO2, CO, CO2, MetanoPropanoCO, LuzUV, MaterialOrganico, CH4, Anemometro, Asociacion, KitNariz

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
admin.site.register(MaterialParticulado)
admin.site.register(NO2)
admin.site.register(Polvo)
admin.site.register(O3)
admin.site.register(SO2)
admin.site.register(CO)
admin.site.register(CO2)
admin.site.register(MetanoPropanoCO)
admin.site.register(LuzUV)
admin.site.register(MaterialOrganico)
admin.site.register(CH4)
admin.site.register(Anemometro)

#modo nariz
admin.site.register(Asociacion)
admin.site.register(KitNariz)






