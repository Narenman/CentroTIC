from django.urls import path 
from . import views
from . import apiviews

app_name = "nariz_electronica"
urlpatterns = [
    path("index", views.index, name="index-nariz"),
    path("lecturas", apiviews.LecturasAPI.as_view()),
    path("analisis", views.analisis_nariz, name="analisis_nariz"),
    path("entrenamiento", views.entrenamiento, name="entrenamiento"),
    path("seleccion_entrenamiento", views.recolectar_datos_entrenamiento, name="seleccion-entrenamiento"),
]
