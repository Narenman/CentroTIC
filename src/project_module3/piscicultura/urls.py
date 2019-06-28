from django.urls import path 
from .views import index, registrar_pozo
from .apiviews import TemperaturaAPIAmbiente, TemperaturaAPIPiscicultura, PhAPIPiscicultura, O2DisueltoAPI, \
                      VoltajeBateriaAPI, PozoAPI

app_name="piscicultura"

urlpatterns = [
   path("index", index, name="index"),
   path("registrar-pozo", registrar_pozo, name="registrar-pozo" ),
   # url para las API
   path("temperatura-pozo", TemperaturaAPIPiscicultura.as_view()),
   path("ph-pozo", PhAPIPiscicultura.as_view()),
   path("oxigeno-disuelto", O2DisueltoAPI.as_view()),
   path("lista-pozos", PozoAPI.as_view()),
]