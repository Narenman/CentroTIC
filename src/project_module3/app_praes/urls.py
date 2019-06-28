from django.urls import path 
from rest_framework.authtoken import views
from .apiviews import TemperaturaAPI, HumedadAPI, PresionAtmosfericaAPI, \
                      O3API, COAPI, CO2API, MetanoPropanoCOAPI, \
                      LuzUVAPI, MaterialOrganicoAPI, CH4API, \
                      CrearUsuarioAPI, LoginView, SensoresAPI, KitNarizAPI

from rest_framework_swagger.views import get_swagger_view
from .views import index, medicion_actual, monitoreo_lecturas, control_ESP32, hora_local, monitoreo_lecturas_json,\
    registros_integrantes, registro_semillero, consultar_semilleros, consultar_integrantes, consulta_temperatura,\
        consulta_humedad, consulta_presion, consulta_luzuv, consulta_co, consulta_co2, consulta_ch4,\
            consulta_o3, consulta_tvoc, consulta_lpg, modo_nariz


app_name = "app_praes"
schema_view = get_swagger_view(title='Estructura API')

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('usuario/', CrearUsuarioAPI.as_view(), name="crear-usuario"),
    path('docs/', schema_view, name="documentacion"),
    path('temperatura/', TemperaturaAPI.as_view(), name="praes-temperatura"),
    path('humedad/', HumedadAPI.as_view(), name="praes-humedad"),
    path('presion-atmosferica/', PresionAtmosfericaAPI.as_view(), name="praes-presion-atmosferica"),
    path('o3/', O3API.as_view(), name="praes-o3"),
    path('co/', COAPI.as_view(), name="praes-co"),
    path('co2/', CO2API.as_view(), name="praes-co2"),
    path('metano-propano-co/', MetanoPropanoCOAPI.as_view(), name="praes-metano-propano-co"),
    path('luz-uv/', LuzUVAPI.as_view(), name="praes-luz-uv"),
    path('material-organico/', MaterialOrganicoAPI.as_view(), name="praes-material-organico"),
    path('ch4/', CH4API.as_view(), name="praes-ch4"),
    path('index/', index, name="index-praes"),
    path('medicion_actual/', medicion_actual, name="medicion-actual"),
    path('monitoreo_lecturas/', monitoreo_lecturas, name="monitoreo-lecturas"),
    path('control_kit/', control_ESP32, name="control-kit"),
    path('sensores/', SensoresAPI.as_view(), name="sensores-API"),
    path('hora-local/', hora_local), 
    path('variables-json/', monitoreo_lecturas_json, name="variables-json"), #para consulta todas variables
    path('registro-integrantes/', registros_integrantes, name="registro-integrantes"),
    path('registro-semillero/', registro_semillero, name="registro-semillero"),
    path('consulta-semillero/', consultar_semilleros, name="consulta-semillero"),
    path('consulta-integrantes/', consultar_integrantes, name="consulta-integrantes"),
    #consultas graficas
    path('json-temperatura/',consulta_temperatura, name="consulta-temperatura"), 
    path('json-humedad/',consulta_humedad, name="consulta-humedad"),
    path('json-presion/', consulta_presion, name="consulta-presion"),
    path('json-luzuv/', consulta_luzuv, name="consulta-luzuv"),
    path('json-co/', consulta_co, name="consulta-co"),
    path('json-co2/', consulta_co2, name="consulta-co2"),
    path('json-ch4/', consulta_ch4, name="consulta-ch4"),
    path('json-o3/', consulta_o3, name="consulta-o3"),
    path('json-tvoc/', consulta_tvoc, name="consulta-tvoc"),
    path('json-lpg/', consulta_lpg, name="consulta-lpg"),
    path("token/", views.obtain_auth_token, name="token"),
    path("modo-nariz/", KitNarizAPI.as_view(), name="modo-nariz"),
    path("kit-nariz/", modo_nariz, name="kit-nariz"),
]