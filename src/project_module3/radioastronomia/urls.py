from django.urls import path
from radioastronomia import views
from .apiviews import AlbumAPI, EspectroAPI

app_name = "radioastronomia"

urlpatterns = [
    path('index', views.index, name="index"),
    path('control-manual', views.control_manual, name="control-manual"),
    path("control-automatico", views.control_automatico, name="control-automatico"),
    path('grafica-espectro', views.json_spectro, name="json-espectro"),
    # APIs para la adquisicion de datos
    path('album-imagenes', AlbumAPI.as_view()),
    path('subsistema-RFI', EspectroAPI.as_view()),
]

