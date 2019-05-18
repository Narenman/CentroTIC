from django import forms 
from .models import Entrenamiento, Analisis

class EntrenamientoForm(forms.ModelForm):

    class Meta:
        model = Entrenamiento
        fields = ('nombre',)

class AnalisisForm(forms.ModelForm):
 
    class Meta:
        model = Analisis
        fields = ('nombre', 'entrenamiento', 'tiempo_medicion_segundos')

class Seleccion_entrenamientoForm(forms.ModelForm):
    class Meta:
        model = Analisis
        fields = ('entrenamiento', )
    



    
