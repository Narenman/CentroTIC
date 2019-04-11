from django import forms 
from .models import DeviceDescriptor, Geolocation,\
    Point, Ellipse, AntennaCharacteristics, FrequencyRange, DeviceOwner


class PointForm(forms.ModelForm):
    
    class Meta:
        model = Point
        fields = ("latitude","longitude")

class EllipseForm(forms.ModelForm):
    
    class Meta:
        model = Ellipse
        fields = ("semi_Major_Axis","semi_Minor_Axis",
        "orientation",)


class GeolocationForm(forms.ModelForm):
    
    class Meta:
        model = Geolocation
        fields = ("confidence",)

class AntennaCharacteristicsForm(forms.ModelForm):
    
    class Meta:
        model = AntennaCharacteristics
        fields = ("height", "height_Type", "antenna_direction", "antenna_radiation_pattern", "antenna_gain")


class FrequencyRangeForm(forms.ModelForm):
    
    class Meta:
        model = FrequencyRange
        fields = ("start_Hz", "stop_Hz",)


class DeviceDescriptorForm(forms.ModelForm):
    
    class Meta:
        model = DeviceDescriptor
        fields = ["serial_Number", "manufacturer_Id", "model_Id", "ruleset_Ids",]


class DeviceOwnerForm(forms.ModelForm):
    
    class Meta:
        model = DeviceOwner
        fields = ("company", "contact", "address", "telephone", "email", "city", "department")