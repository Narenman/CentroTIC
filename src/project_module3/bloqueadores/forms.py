from django import forms 
from .models import UsuariosPrimarios

class UsuariosPrimariosForm(forms.ModelForm):
    
    class Meta:
        model = UsuariosPrimarios
        fields = ("ciudad",)
