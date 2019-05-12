from django.urls import path 
from . import views

app_name = "paws"
urlpatterns = [
    path("index", views.index, name="index-paws"),
    path("register", views.register, name="register"),
    path("ayuda-formulario", views.documentacion_registro, name="ayuda"),
    path("avail-spectrum", views.avail_spectrum, name="avail-spectrum"),
    path("dispositivos-validados", views.dispositivos_validados, name="dispositivos-validados"),
    path("canales-regiones", views.canales_regiones, name="canales-regiones"),
]
