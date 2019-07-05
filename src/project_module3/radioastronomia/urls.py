from django.urls import path
from .views import control_manual, index
from .apiviews import AlbumAPI, EspectroAPI

app_name = "radioastronomia"

urlpatterns = [
    path('index', index, name="index"),
    path('control-manual', control_manual, name="control-manual"),
    # APIs para la adquisicion de datos
    path('album-imagenes', AlbumAPI.as_view()),
    path('subsistema-RFI', EspectroAPI.as_view()),
]

