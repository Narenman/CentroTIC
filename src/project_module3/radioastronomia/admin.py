from django.contrib import admin

# Register your models here.
from .models import AlbumImagenes, RegionCampana, Estado, CaracteristicasAntena, Espectro

admin.site.register(AlbumImagenes)
admin.site.register(RegionCampana)
admin.site.register(Estado)
admin.site.register(CaracteristicasAntena)
admin.site.register(Espectro)