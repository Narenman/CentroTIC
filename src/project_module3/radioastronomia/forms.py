from django import forms
from .models import Espectro

class EspectroForm(forms.ModelForm):  
    class Meta:
        model = Espectro
        fields = ("frec_muestreo", "nfft", "frec_central", "region")

class RegionForm(forms.ModelForm):
    class Meta:
        model = Espectro
        fields = ("region",)


class RFIForm(forms.Form):
    frecuencia_inicial = forms.IntegerField(required=False)
    frecuencia_final = forms.IntegerField(required=False)
    frecuencia_muestreo = forms.IntegerField(required=False)
    nfft = forms.IntegerField(required=False)

