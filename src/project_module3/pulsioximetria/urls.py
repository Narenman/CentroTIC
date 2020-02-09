from django.urls import path 
from pulsioximetria import views
from django.views.generic import TemplateView
from pulsioximetria import apiviews
from  .views import datos_json_pulso, datos_json_all



app_name = "pulsioximetria"
urlpatterns = [
    path("index/", TemplateView.as_view(template_name="pulsioximetria/index.html"), name="index"),
    path("patologias/", TemplateView.as_view(template_name="pulsioximetria/insurance.html"), name="patologias"),
    path("pacientes/", TemplateView.as_view(template_name="pulsioximetria/packages.html"), name="pacientes"),
    #API
    path("lecturas", apiviews.LecturasAPI.as_view()),
    path("datosgraf-json", datos_json_pulso, name= "datosgraf-json"),
    path("datos-json-all", datos_json_all, name="datos-json-all"),
]
