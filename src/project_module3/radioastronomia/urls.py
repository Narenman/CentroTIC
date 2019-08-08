from django.urls import path
from django.views.generic import TemplateView

from radioastronomia import views
from .apiviews import AlbumAPI, EspectroAPI, CaracteristicasEspectroAPI, EstadoAPI

app_name = "radioastronomia"

urlpatterns = [
    #urls para informacion
    path('index', views.index, name="index"),
    path('lista/antenas', views.CaracteristicasAntenaListView.as_view(), name="antenas"),
    path('crear/antenas', views.CaracteristicasAntenaCreateView.as_view(), name="crear-antena"),
    path('actualizar/antena/<int:pk>', views.CaracteristicasAntenaUpdateView.as_view(), name="actualizar-antena"),
    path('borrar/antena/<int:pk>', views.CaracteristicasAntenaDeleteView.as_view(), name="borrar-antena"),
    path('subsistema/RFI', TemplateView.as_view(template_name="radioastronomia/subsistema_RFI.html"), name="subsistema-RFI"),
    #urls para operacion del sistema
    path('control-manual', views.control_manual, name="control-manual"),
    path("control-automatico", views.control_automatico, name="control-automatico"),
    # urls para graficas
    path('grafica-espectro', views.json_spectro, name="json-espectro"),
    # APIs para la adquisicion de datos
    path('album-imagenes', AlbumAPI.as_view()),
    path('subsistema-RFI', EspectroAPI.as_view()),
    path('caracteristicas-espectro', CaracteristicasEspectroAPI.as_view()),
    path('estado/<int:pk>', EstadoAPI.as_view()),
]

