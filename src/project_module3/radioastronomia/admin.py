from django.contrib import admin

# Register your models here.
from .models import AlbumImagenes, RegionCampana, Estado, CaracteristicasAntena

admin.site.register(AlbumImagenes)
admin.site.register(RegionCampana)
admin.site.register(Estado)
admin.site.register(CaracteristicasAntena)