from django.shortcuts import render
from django.http import JsonResponse
from .forms import  GeolocationForm, DeviceValidityForm, \
    FrequencyRangeForm, DeviceDescriptorForm, DeviceOwnerForm

from .models import DeviceDescriptor, Geolocation, SpectrumSpec, DeviceValidity

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
    freq_range = FrequencyRangeForm()
    device_descriptor = DeviceDescriptorForm()
    device_owner = DeviceOwnerForm()
    device_validity = DeviceValidityForm()
    print(request.POST)
    if request.POST:
        freq_range = FrequencyRangeForm(request.POST)
        device_descriptor = DeviceDescriptorForm(request.POST)
        device_owner = DeviceOwnerForm(request.POST)
        
        device_validity = DeviceValidityForm(request.POST)

        if device_validity.is_valid() or freq_range.is_valid() and device_descriptor.is_valid() and device_owner.is_valid():

            device_descriptor = device_descriptor.save(commit=False)
            device_descriptor.device_capabilities = freq_range.save()
            device_descriptor.save()

            device_owner = device_owner.save(commit=False)
            device_owner.device_descriptor = device_descriptor
            device_owner.save()
            # device_validity = device_validity.save(commit=False)
            # device_validity.device_descriptor = device_descriptor
            # device_validity.save()

            return render(request, "paws/registro_exitoso.html", {"registro": "Registro exitoso de dispositivo"})

    respuesta = {"freq_range": freq_range,
                 "device_descriptor": device_descriptor,
                 "device_owner": device_owner,
                 "device_validity":device_validity,}

    return render(request, "paws/register.html", respuesta)

def avail_spectrum(request):
    """Esta funcion se realiza con el fin de retornar AVAIL_SPECTRUM_RESP
    """
    #bases de datos que se consultan de acuerdo a las peticiones del maestro
    device = DeviceDescriptor.objects.all()
    geolocation = Geolocation.objects.all() 
    device_descriptor = device.values('serial_Number' ,  'manufacturer_Id' , 
                        'model_Id','device_capabilities', 'geolocation' )

    #base de datos del espectro consultada y filtrada de acuerdo a la informacion
    #georeferenciada del maestro

    spectrum = SpectrumSpec.objects.all()
    try:
        #formacion de la respuesta AVAIL_SPECTRUM_RESP
        avail_spectrum_resp = {"serial_Number": device_descriptor[0]["serial_Number"],
                            "manufacturer_Id":device_descriptor[0]["manufacturer_Id"],
                            "model_Id": device_descriptor[0]["model_Id"], "ruleset_Ids": device_descriptor[0]["ruleset_Ids"],
                            "device_capabilities":device_descriptor[0]["device_capabilities"]}
    except:
        avail_spectrum_resp = {}

    return JsonResponse(avail_spectrum_resp)

def dispositivos_validados(request):
    dispositivos = DeviceValidity.objects.all()
    devices = dispositivos.values("deviceDesc", "isValid", "reason")
    disp = list(map(lambda devices: devices["deviceDesc"], devices))
    devicesdescp = DeviceDescriptor.objects.filter(pk__in=disp)
    geo_device=devicesdescp.values("geolocation")

    geolocation = Geolocation.objects.filter(pk__in=geo_device)
    geo_device = geolocation.values("city")

    for i in range(len(devices)):
        devices[i]["deviceDesc"]=devicesdescp[i]
        devices[i].update({"geolocation": geo_device[i]})
    print(devices)
    return render(request, "paws/dispositivos_validados.html", {"devices": devices})