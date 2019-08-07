from django.urls import path
from django.views.generic import TemplateView

from rest_framework.authtoken import views as view
from rest_framework_swagger.views import get_swagger_view

from app_praes import views
from app_praes import apiviews

app_name = "app_praes"
schema_view = get_swagger_view(title='Estructura API')

urlpatterns = [
    path('index/', TemplateView.as_view(template_name="app_praes/index.html"), name="index-praes"),
    path('docs/', schema_view, name="documentacion"),
    path("lista/lugares", views.Ubicacion_lecturaListView.as_view(), name="lugares"),
    path("lugar/<int:pk>/delete/", views.Ubicacion_lecturaDeleteView.as_view(), name="borrar"),
    path("registro/", views.Ubicacion_lecturaCreateView.as_view(), name="registro"),
    path("semilleros/", views.SemilleroListView.as_view(), name="semilleros"),
    path("semillero/<int:pk>/borrar", views.SemilleroDeleteView.as_view(), name="borrar-semillero"),
    path("semillero/crear", views.SemilleroCreateView.as_view(), name="registro-semillero"),
    path("lista/colegios", views.ColegioListView.as_view(), name="colegios"),
    path("registro/colegio", views.ColegioCreateView.as_view(), name="registro-colegios"),
    path("actualizar/colegio/<int:pk>", views.ColegioUpdateView.as_view(), name="actualizar-colegio"),
    path("lista/kits", views.KitListView.as_view(), name="consulta-kits"),
    path("registro/kit", views.KitCreateView.as_view(), name="registro-kit"),
    
    #APIS
    path('login/', apiviews.LoginView.as_view(), name="login"),
    path('usuario/', apiviews.CrearUsuarioAPI.as_view(), name="crear-usuario"),
    path('temperatura/', apiviews.TemperaturaAPI.as_view(), name="praes-temperatura"),
    path('humedad/', apiviews.HumedadAPI.as_view(), name="praes-humedad"),
    path('presion-atmosferica/', apiviews.PresionAtmosfericaAPI.as_view(), name="praes-presion-atmosferica"),
    path("modo-nariz/", apiviews.CalidadAireAPI.as_view(), name="modo-nariz"),
    path("ph-agua/", apiviews.PHAPI.as_view(), name="ph-API"),
    path("temperatura-agua/", apiviews.TemperaturaAguaAPI.as_view()),
    path("turbidez-agua/", apiviews.TurbidezAguaAPI.as_view()),
    path("flujo-agua", apiviews.FlujoAguaAPI.as_view()),
    path("registro-kit", apiviews.KITAPI.as_view(), name="kit"),

    #informacion de variables medidas por el kit
    path('medicion_actual/', views.medicion_actual_temperatura, name="medicion-actual"),
    path("medicion_actual_humedad/", views.medicion_actual_humedad, name="medicion-humedad"),
    path("medicion_actual_presion/", views.medicion_actual_presion, name="medicion-presion"),
    path("medicion_compuestos_aire", views.medicion_compuestos_aire, name="medicion-compuestos-aire"),
    path("medicion_ph_agua", views.medicion_ph_agua, name="medicion-ph-agua"),
    path("medicion_turbidez", views.medicion_turbidez, name="medicion-turbidez"),
    path("medicion_temperatura_agua/", views.medicion_temperatura_agua, name="medicion-temp-agua"),
    path("medicion_flujo/", views.medicion_flujo_agua, name="medicion-flujo"),
    path("matematica-ambiental/", views.matematica_ambiental, name="matematica-ambiental"),

    path("descargar-datos/", views.descargar, name="descargar"),

    #consultas graficas
    path('json-temperatura/',views.consulta_temperatura, name="consulta-temperatura"), 
    path('json-humedad/',views.consulta_humedad, name="consulta-humedad"),
    path('json-presion/', views.consulta_presion, name="consulta-presion"),
    path('json-ph/', views.consulta_ph, name="consulta-ph"),
    path('json-turbidez/', views.consulta_turbidez, name="consulta-turbidez"),
    path('json-temp-agua/', views.consulta_temp_agua, name="consulta-temp-agua"),
    path('json-flujo/', views.consulta_flujo, name="consulta-flujo"),
    path('json-aire/', views.consulta_compuestos_aire, name="consulta-aire"),
    path("token/", view.obtain_auth_token, name="token"),
]