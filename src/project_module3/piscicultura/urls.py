from django.urls import path 
#from .views import index, registrar_pozo
from .views import index, registrar_pozo, toma_datos, monitoreo, json_last_est1, json_last_est2, json_last_est3, json_all_est1, json_all_est2,json_all_est3, json_estado


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
   path("json-last-est1/", json_last_est1, name="json-last-est1"),
   path("json-last-est2/", json_last_est2, name="json-last-est2"), 
   path("json-last-est3/", json_last_est3, name="json-last-est3"),
   path("json-all-est1/", json_all_est1, name="json-all-est1"), 
   path("json-all-est2/", json_all_est2, name="json-all-est2"), 
   path("json-all-est3/", json_all_est3, name="json-all-est3"), 

   path("json-estado", json_estado, name="json-estado"),
]
