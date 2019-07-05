from django.contrib import admin

# Register your models here.
from .models import AlbumImagenes, RegionCampana

admin.site.register(AlbumImagenes)
admin.site.register(RegionCampana)