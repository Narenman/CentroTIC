from django import forms
from .models import Pozo

class PozoForm(forms.ModelForm):
    
    class Meta:
        model = Pozo
        fields = ("nombre","area","cantidad_peces","ubicacion")
