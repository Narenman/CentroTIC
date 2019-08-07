from django import forms 
from .models import Semillero, Temperatura, Ubicacion_lectura


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Temperatura
        fields = ("ubicacion","kit_monitoreo")

class UbicacionLecturasForm(forms.ModelForm):
    class Meta:
        model = Ubicacion_lectura
        fields = ("etiqueta_ubicacion","tipo_experimento")
