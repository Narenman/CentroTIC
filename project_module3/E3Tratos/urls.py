from django.urls import path 
from .apiviews import VariablesAPI
from .views import index, datos_json, gui, docs, media, contact

app_name = "E3Tratos"

urlpatterns = [
        path("variables-api", VariablesAPI.as_view(),name="e3tratos-api"),
        path("home", index, name="index-E3Tratos"),
        path("datos-json", datos_json, name="datos-json-E3Tratos"),
        path("GUI", gui, name="tratosgui"),
        path("docs", docs, name="tratosdocs"),
        path("media", media, name="tratosmedia"),
        path("contact", contact, name="tratoscontact"),
]
