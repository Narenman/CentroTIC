from django.contrib import admin
from .models import Espectro, UsuariosPrimarios, Dispositivos, Ciudad
# Register your models here.

admin.site.register(Espectro)
admin.site.register(Ciudad)
admin.site.register(UsuariosPrimarios)
admin.site.register(Dispositivos)