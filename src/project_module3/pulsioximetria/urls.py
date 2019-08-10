from django.urls import path 
from pulsioximetria import views
from django.views.generic import TemplateView
from pulsioximetria import apiviews


app_name = "pulsioximetria"
urlpatterns = [
    path("index/", TemplateView.as_view(template_name="pulsioximetria/index.html"), name="index"),
    path("patologias/", TemplateView.as_view(template_name="pulsioximetria/insurance.html"), name="patologias"),
    path("pacientes/", TemplateView.as_view(template_name="pulsioximetria/packages.html"), name="pacientes"),
    #API
    path("lecturas", apiviews.LecturasAPI.as_view()),
]
