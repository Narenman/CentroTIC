from django.urls import path 
from . import views

app_name = "bloqueadores"
urlpatterns = [
    path("index", views.index, name="index"),
    path("jamming", views.jamming, name="jamming"),
    path("monitoring", views.monitoring, name="monitoring"),
    path("consulta-usuarios", views.consulta_usuarios_primarios, name="consulta-usuarios"),
]
