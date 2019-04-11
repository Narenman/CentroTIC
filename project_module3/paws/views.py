from django.shortcuts import render
from .forms import  PointForm, EllipseForm, \
    GeolocationForm, AntennaCharacteristicsForm, \
    FrequencyRangeForm, DeviceDescriptorForm, DeviceOwnerForm

# Create your views here.
def index(request):
    respuesta = {}
    return render(request, "paws/index.html", respuesta)

def documentacion_registro(request):
    return render(request, "paws/recomendacion_registro.html", {})

def register(request):
    """ esta funcion se encarga de realizar el 
    REGISTRATION_REQ mediante un formulario web
    """
    point = PointForm()
    ellipse = EllipseForm()
    geolocation = GeolocationForm()
    antenna = AntennaCharacteristicsForm()
    freq_range = FrequencyRangeForm()
    device_descriptor = DeviceDescriptorForm()
    device_owner = DeviceOwnerForm()

    if request.POST:
        point = PointForm(request.POST, )
        ellipse = EllipseForm(request.POST, )
        geolocation = GeolocationForm(request.POST,)
        antenna = AntennaCharacteristicsForm(request.POST)
        freq_range = FrequencyRangeForm(request.POST)
        device_descriptor = DeviceDescriptorForm(request.POST)
        device_owner = DeviceOwnerForm(request.POST)

        if point.is_valid() and ellipse.is_valid() and geolocation.is_valid() and antenna.is_valid() and freq_range.is_valid() and device_descriptor.is_valid() and device_owner.is_valid():
            ellipse = ellipse.save(commit=False)
            ellipse.center = point.save()
            ellipse.save()

            geolocation = geolocation.save(commit=False)
            geolocation.point =  ellipse
            geolocation.save()

            device_descriptor = device_descriptor.save(commit=False)
            device_descriptor.anttenna_characteristics = antenna.save()
            device_descriptor.device_capabilities = freq_range.save()
            device_descriptor.geolocation = geolocation
            device_descriptor.save()

            device_owner = device_owner.save(commit=False)
            device_owner.device_descriptor = device_descriptor
            device_owner.save()

            return render(request, "paws/index.html", {})

    respuesta = {"point": point,
                 "ellipse": ellipse,
                 "geolocation": geolocation,
                 "antenna": antenna, 
                 "freq_range": freq_range,
                 "device_descriptor": device_descriptor,
                 "device_owner": device_owner}

    return render(request, "paws/register.html", respuesta)