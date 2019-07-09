from django.contrib import admin
from .models import Departamento, Ciudad, Kit, Colegio, Sensores, Semillero, Temperatura, \
    Humedad, PresionAtmosferica, Asociacion, KitNariz

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


#modo nariz
admin.site.register(Asociacion)
admin.site.register(KitNariz)






