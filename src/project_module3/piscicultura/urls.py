from django.urls import path 
#from .views import index, registrar_pozo
from .views import index, registrar_pozo, toma_datos, monitoreo, last_json_data, lecturas_json_all, json_estado
from .apiviews import TemperaturaAPICaja, HumedadAPICaja, TemperaturaAPIPiscicultura, PhAPIPiscicultura, O2DisueltoAPI, \
                      VoltajeBateriaAPI, PozoAPI

app_name="piscicultura"

urlpatterns = [
   path("index", index, name="index"),
   path("registrar-pozo", registrar_pozo, name="registrar-pozo" ),
   # url para las API
   path("temperatura-pozo", TemperaturaAPIPiscicultura.as_view()),
   path("temperatura-caja", TemperaturaAPICaja.as_view()),
   path("humedad-caja", HumedadAPICaja.as_view()),
   path("ph-pozo", PhAPIPiscicultura.as_view()),
   path("oxigeno-disuelto", O2DisueltoAPI.as_view()),
   path("voltaje-bateria", VoltajeBateriaAPI.as_view()),
   path("lista-pozos", PozoAPI.as_view()),
   ####
   path("monitoreo", monitoreo, name="monitoreo"),
   path("toma-datos", toma_datos, name="toma-datos"),
   path("variables-json-last/", last_json_data, name="variables-json-last"), 
   path("variables-json-all/", lecturas_json_all, name="variables-json-all"), 
   path("json-estado", json_estado, name="json-estado"),
]
