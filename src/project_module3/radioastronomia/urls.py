from django.urls import path
from django.views.generic import TemplateView

from radioastronomia import views
from radioastronomia import apiviews

app_name = "radioastronomia"

urlpatterns = [
    #urls para informacion
    path('index', views.RegionCampanaListView.as_view(), name="index"),
    path('lista/antenas', views.CaracteristicasAntenaListView.as_view(), name="antenas"),
    path('lista/rbw', views.RBWListView.as_view(), name="rbw"),
    path('crear/antenas', views.CaracteristicasAntenaCreateView.as_view(), name="crear-antena"),
    path('crear/sensores', views.CaracteristicasEstacionCreateView.as_view(), name="crear-sensor"),
    # path('crear/RBW', views.RBWCreateView.as_view(), name="crear-rbw"),
    path('crear/RBW', views.RBWcreate, name="crear-rbw"),
    path('crear/region', views.RegionCreateView.as_view(), name="crear-region"),
    path('actualizar/antena/<int:pk>', views.CaracteristicasAntenaUpdateView.as_view(), name="actualizar-antena"),
    path('actualizar/sensor/<int:pk>', views.CaracteristicasEstacionUpdateView.as_view(), name="actualizar-sensor"),
    path('actualizar/rbw/<int:pk>', views.RBWUpdateView.as_view(), name="actualizar-rbw"),
    path('borrar/antena/<int:pk>', views.CaracteristicasAntenaDeleteView.as_view(), name="borrar-antena"),
    path('borrar/sensor/<int:pk>', views.CaracteristicasEstacionDeleteView.as_view(), name="borrar-sensor"),
    path('borrar/rbw/<int:pk>', views.RBWDeleteView.as_view(), name="borrar-rbw"),
    # subsistemas
    path('subsistema/RFI', TemplateView.as_view(template_name="radioastronomia/subsistema_RFI.html"), name="subsistema-RFI"),
    path('subsistema/estacion-monitoreo',views.CaracteristicasEstacionListView.as_view(), name="subsistema-estacion"),
    path('subsistema/camara', views.subsistemacielo, name="subsistema-camara"),
    #urls para operacion del sistema
    path('control-manual', views.control_manual, name="control-manual"),
    path("control-automatico", views.control_automatico, name="control-automatico"),
    path("detener", views.detener, name="detener"),
    # urls para graficas
    path('grafica-espectro', views.json_spectro, name="json-espectro"),
    path('barrido-espectro', views.barrido_json, name="barrido-espectro"),
    path('posiciones-angulares', views.espectro_angulos, name="posiciones-angulares"),
    path('monitoreo-ambiental', views.json_estacion, name="monitor-ambiental"),
    # APIs para la adquisicion de datos
    path('album-imagenes', apiviews.AlbumAPI.as_view()),
    path('subsistema-RFI', apiviews.EspectroAPI.as_view()),
    path('caracteristicas-espectro', apiviews.CaracteristicasEspectroAPI.as_view()),
    path('estado/<int:pk>', apiviews.EstadoAPI.as_view()),
    path('posicion-antena', apiviews.PosicionAntenaAPI.as_view()),
    path('estacion-monitoreo', apiviews.EstacionAmbientalAPI.as_view()),
    # modos de procesamiento del espectro
    path('modo/bandas-espectrales', views.bandas_espectrales, name="modo1"),
    path('modo/analisis-tiempo',views.analisis_tiempo, name="modo2"),
    path('modo/analisis-angular', views.analisis_angular, name="modo3"),
    path('modo/comparacion-zonas', views.comparacion_zonas, name="modo4"),
]

