"""project_module3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_sensado import views

#static and media
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.main_index, name='main-index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('app_sensado/', include('app_sensado.urls', namespace='app_sensado')),
    path('app_praes/', include('app_praes.urls', namespace="app_praes")),
    path('paws/', include('paws.urls', namespace="paws")),
    path('nariz_electronica/', include('nariz_electronica.urls', namespace="nariz_electronica")),
    path('E3Tratos/', include('E3Tratos.urls', namespace="E3Tratos")),
    path('nariz_electronicaV2/', include('nariz_electronica2.urls', namespace="nariz_electronicaV2")),
    path('piscicultura/', include('piscicultura.urls', namespace="piscicultura")),
    path('bloqueadores/', include('bloqueadores.urls', namespace="bloqueadores")),
    path('radioastronomia/', include('radioastronomia.urls', namespace="radioastronomia")),
    path('particulado/', include('particulado.urls', namespace="particulado")),
    path('pulsioximetria/', include('pulsioximetria.urls', namespace="pulsioximetria")),
    path('bicicletas/', include('bicicletas.urls', namespace="bicicletas")),
]

#para los archivos de media
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)