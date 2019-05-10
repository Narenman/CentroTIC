from django import forms 
from .models import DeviceDescriptor, Geolocation, FrequencyRange, \
     DeviceOwner, DeviceValidity

class GeolocationForm(forms.ModelForm):
    
    class Meta:
        model = Geolocation
        fields = ("region","city","dane_code")

class FrequencyRangeForm(forms.ModelForm):
    
    class Meta:
        model = FrequencyRange
        fields = ("start_Hz", "stop_Hz",)


class DeviceDescriptorForm(forms.ModelForm):
    
    class Meta:
        model = DeviceDescriptor
        fields = ["serial_Number", "manufacturer_Id", "model_Id", "ruleset_Ids","geolocation"]


class DeviceOwnerForm(forms.ModelForm):
    
    class Meta:
        model = DeviceOwner
        fields = ("company", "contact", "telephone", "email")


class DeviceValidityForm(forms.ModelForm):
    
    class Meta:
        model = DeviceValidity
        fields = ("reason","isValid")
    
