from django.urls import path 
from . import views
from .apiviews import EspectroAPI

app_name = "bloqueadores"
urlpatterns = [
    path("index", views.index, name="index"),
    path("jamming", views.jamming, name="jamming"),
    path("monitoring", views.monitoring, name="monitoring"),
    path("consulta-usuarios", views.consulta_usuarios_primarios, name="consulta-usuarios"),
    path("registrar-dispositivos", views.registrar_dispositivos, name="registrar-dispositivos"),
    path("consulta-dispositivos", views.consulta_dispositivos, name="consulta-dispositivos"),
    path("espectro/<int:pk>", EspectroAPI.as_view()),
    path("espectro-json", views.espectro_json, name="espectro-json"),
    path("grafica-espectro", views.grafica_espectro, name="grafica-espectro"),
]
