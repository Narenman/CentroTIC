from django.urls import path
from django.views.generic import TemplateView

from radioastronomia import views
from radioastronomia import apiviews

app_name = "radioastronomia"

urlpatterns = [
    #urls para informacion
    path('index', TemplateView.as_view(template_name="radioastronomia/index.html"), name="index"),
    path('lista/antenas', views.CaracteristicasAntenaListView.as_view(), name="antenas"),
    path('lista/rbw', views.RBWListView.as_view(), name="rbw"),
    path('crear/antenas', views.CaracteristicasAntenaCreateView.as_view(), name="crear-antena"),
    path('crear/sensores', views.CaracteristicasEstacionCreateView.as_view(), name="crear-sensor"),
    path('crear/RBW', views.RBWCreateView.as_view(), name="crear-rbw"),
    path('actualizar/antena/<int:pk>', views.CaracteristicasAntenaUpdateView.as_view(), name="actualizar-antena"),
    path('actualizar/sensor/<int:pk>', views.CaracteristicasEstacionUpdateView.as_view(), name="actualizar-sensor"),
    path('borrar/antena/<int:pk>', views.CaracteristicasAntenaDeleteView.as_view(), name="borrar-antena"),
    path('borrar/sensor/<int:pk>', views.CaracteristicasEstacionDeleteView.as_view(), name="borrar-sensor"),
    path('subsistema/RFI', TemplateView.as_view(template_name="radioastronomia/subsistema_RFI.html"), name="subsistema-RFI"),
    path('subsistema/estacion-monitoreo',views.CaracteristicasEstacionListView.as_view(), name="subsistema-estacion") ,
    #urls para operacion del sistema
    path('control-manual', views.control_manual, name="control-manual"),
    path("control-automatico", views.control_automatico, name="control-automatico"),
    # urls para graficas
    path('grafica-espectro', views.json_spectro, name="json-espectro"),
    path('barrido-espectro', views.barrido_json, name="barrido-espectro"),
    # APIs para la adquisicion de datos
    path('album-imagenes', apiviews.AlbumAPI.as_view()),
    path('subsistema-RFI', apiviews.EspectroAPI.as_view()),
    path('caracteristicas-espectro', apiviews.CaracteristicasEspectroAPI.as_view()),
    path('estado/<int:pk>', apiviews.EstadoAPI.as_view()),
    # modos de procesamiento del espectro
    path('modo/bandas-espectrales', views.bandas_espectrales, name="modo1"),
]

