from django.urls import path 
from rest_framework.authtoken import views
from .apiviews import TemperaturaAPI, HumedadAPI, PresionAtmosfericaAPI, \
                      CrearUsuarioAPI, LoginView, SensoresAPI, KitNarizAPI

from rest_framework_swagger.views import get_swagger_view
from .views import index, medicion_actual_temperatura, monitoreo_lecturas, control_ESP32, hora_local, monitoreo_lecturas_json,\
    registros_integrantes, registro_semillero, consultar_semilleros, consultar_integrantes, consulta_temperatura,\
        consulta_humedad, consulta_presion, modo_nariz, medicion_actual_humedad, medicion_actual_presion, medicion_compuestos_aire, \
            medicion_ph_agua, consulta_ph, medicion_turbidez, consulta_turbidez, medicion_temperatura_agua, consulta_temp_agua, \
                medicion_flujo_agua, consulta_flujo


app_name = "app_praes"
schema_view = get_swagger_view(title='Estructura API')

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('usuario/', CrearUsuarioAPI.as_view(), name="crear-usuario"),
    path('docs/', schema_view, name="documentacion"),
    path('temperatura/', TemperaturaAPI.as_view(), name="praes-temperatura"),
    path('humedad/', HumedadAPI.as_view(), name="praes-humedad"),
    path('presion-atmosferica/', PresionAtmosfericaAPI.as_view(), name="praes-presion-atmosferica"),
    path('index/', index, name="index-praes"),

    #informacion de variables medidas por el kit
    path('medicion_actual/', medicion_actual_temperatura, name="medicion-actual"),
    path("medicion_actual_humedad/", medicion_actual_humedad, name="medicion-humedad"),
    path("medicion_actual_presion/", medicion_actual_presion, name="medicion-presion"),
    path("medicion_compuestos_aire", medicion_compuestos_aire, name="medicion-compuestos-aire"),
    path("medicion_ph_agua", medicion_ph_agua, name="medicion-ph-agua"),
    path("medicion_turbidez", medicion_turbidez, name="medicion-turbidez"),
    path("medicion_temperatura_agua/", medicion_temperatura_agua, name="medicion-temp-agua"),
    path("medicion_flujo/", medicion_flujo_agua, name="medicion-flujo"),

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
    path('json-ph/', consulta_ph, name="consulta-ph"),
    path('json-turbidez/', consulta_turbidez, name="consulta-turbidez"),
    path('json-temp-agua/', consulta_temp_agua, name="consulta-temp-agua"),
    path('json-flujo/', consulta_flujo, name="consulta-flujo"),
    path("token/", views.obtain_auth_token, name="token"),
    path("modo-nariz/", KitNarizAPI.as_view(), name="modo-nariz"),
    path("kit-nariz/", modo_nariz, name="kit-nariz"),
]