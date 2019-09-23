from django.urls import path 
from django.views.generic import TemplateView

from particulado import views
from particulado import apiviews

app_name = "particulado"
urlpatterns = [
    path("index", views.index, name="index"),
    #para las plantillas sin views.py
    path("grafica-pms", TemplateView.as_view(template_name="particulado/grafica_pms.html"), name="grafica-pms"),
    path("tabla", TemplateView.as_view(template_name="particulado/grafica_opc.html"), name="tabla"),
    path("grafica-opc", TemplateView.as_view(template_name="particulado/grafica_opc.html"),name="grafica-opc"),
    #registro de apis
    path("pms1", apiviews.Pms5003aAPI.as_view()),
    path("pms2", apiviews.Pms5003bAPI.as_view()),
    #para las graficas
    path("jsonA", views.json_pmsA, name="jsonA"),
    path("jsonB", views.json_pmsB, name="jsonB"),

]
