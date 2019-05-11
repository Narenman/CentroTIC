from django.urls import path 
from . import views

app_name = "nariz_electronicaV2"
urlpatterns = [
    path("index", views.index, name="index"),
    path("control-nariz", views.control_narizV2, name="control-nariz"),
]
