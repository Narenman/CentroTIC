from django.urls import path
from django.views.generic import TemplateView

app_name = "bicicletas"

urlpatterns = [
    path("index", TemplateView.as_view(template_name="bicicletas/index.html"), name="index")
]
