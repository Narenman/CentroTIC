from django import forms 
from .models import UsuariosPrimarios, Dispositivos

class UsuariosPrimariosForm(forms.ModelForm):
    
    class Meta:
        model = UsuariosPrimarios
        fields = ("ciudad",)

class DispositivosForm(forms.ModelForm):
    
    class Meta:
        model = Dispositivos
        fields = ("modelo_id","ubicacion", "ciudad")

