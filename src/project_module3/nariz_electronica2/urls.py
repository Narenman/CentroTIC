from django.urls import path 
from django.views.generic import TemplateView

from nariz_electronica2 import views, apiviews

app_name = "nariz_electronicaV2"
urlpatterns = [
    path("index", views.index, name="index"),
    #path("control-nariz", views.control_narizV2, name="control-nariz"),
   
    #para las plantillas sin views.py
    path("grafica-mq", TemplateView.as_view(template_name="nariz_electronicaV2/grafica_mq.html"), name="grafica-mq"),
	
	#registro de apis
    path("mq", apiviews.SENSORES4API.as_view()),
    
    #para las graficas
    path("jsonA", views.json_mq, name="jsonA"),
]
