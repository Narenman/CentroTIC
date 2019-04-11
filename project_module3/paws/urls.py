from django.urls import path 
from . import views

app_name = "paws"
urlpatterns = [
    path("index", views.index, name="index-paws"),
    path("register", views.register, name="register"),
    path("ayuda-formulario", views.documentacion_registro, name="ayuda"),
]
