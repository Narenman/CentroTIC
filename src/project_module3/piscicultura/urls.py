from django.urls import path 
from .views import index

app_name="piscicultura"

urlpatterns = [
   path("index", index, name="index")
]