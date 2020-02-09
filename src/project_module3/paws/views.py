from django.shortcuts import render
from django.http import JsonResponse
from .forms import  GeolocationForm, DeviceValidityForm, \
    FrequencyRangeForm, DeviceDescriptorForm, DeviceOwnerForm, SpectrumForm

from .models import DeviceDescriptor, Geolocation, SpectrumSpec, DeviceValidity, \
    Spectrum, Frequency, RulsetInfo
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    respuesta = {}
    return render(request, "paws/index.html", respuesta)

def documentacion_registro(request):
    return render(request, "paws/recomendacion_registro.html", {})

def dispositivos_validados(request):
    """Consulta la lista de dispositivos validados y no validados """
    devicevalidity = DeviceValidity.objects.all()
    devices = devicevalidity.values("deviceDesc", "isValid", "reason")
    for data in devices:
        id_deviceDesc = data["deviceDesc"]
        devicesDesc = DeviceDescriptor.objects.get(pk=id_deviceDesc)
        data.update({"geolocation": devicesDesc.geolocation , "serial":devicesDesc.serial_Number})
        # print(devicesDesc.geolocation)
    # print(devices)
    return render(request, "paws/dispositivos_validados.html", {"devices": devices})

def canales_regiones(request):
    """ Como informacion util del lado del cliente, para el maestro
    se necesita hacer otro proceso
    """
    spectrum_form = SpectrumForm() # este formulario es para mostrar la lista de regiones a partir de codigo DANE
    if request.POST:
        spectrum = Spectrum.objects.filter(geolocation=request.POST["geolocation"]) # filtra el espectro de acuerdo al codigo DANE
        spectrum = spectrum.values("operation", "channels")
        geolocation = Geolocation.objects.get(pk=request.POST["geolocation"])
        # print(geolocation.region)
        datos = {"canales_ocupados": spectrum, "spectrum_form": spectrum_form,
            "ciudad": geolocation.city, "departamento": geolocation.region}
    else:
        datos = {"spectrum_form": spectrum_form}
    return render(request, "paws/canales_regiones.html",datos)

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

            device_validity = device_validity.save(commit=False)
            device_validity.deviceDesc = device_descriptor
            device_validity.save()

            return render(request, "paws/registro_exitoso.html", {"registro": "Registro exitoso de dispositivo", "info_reg":request.POST})

    respuesta = {"freq_range": freq_range,
                 "device_descriptor": device_descriptor,
                 "device_owner": device_owner,
                 "device_validity":device_validity,}

    return render(request, "paws/register.html", respuesta)

#Operaciones del protocolo entre el maestro y el esclavo
@csrf_exempt
def init_req(request):
    """ Es la funcion que da inicio al protocolo PAWS """
    master_data = request.POST    
    device = DeviceDescriptor.objects.filter(serial_Number=master_data["serial_Number"]).filter(model_Id=master_data["model_Id"])
    if len(device) >= 1:
        spectrumspec = SpectrumSpec.objects.filter(geolocation=master_data["dane_code"])
        ruleset_id = spectrumspec.values("rulset_Info")
        ruleset_id = ruleset_id[0]
        ruleset_id = ruleset_id["rulset_Info"]
        print(ruleset_id)
        ruleset_info = RulsetInfo.objects.filter(pk=ruleset_id)
        ruleset_info = list(ruleset_info.values("authority", "rulsetId"))
        INIT_RESP = {"ruleset_info":ruleset_info}
    return JsonResponse(INIT_RESP)


@csrf_exempt
def avail_spectrum(request):
    """Esta funcion se realiza con el fin de retornar AVAIL_SPECTRUM_RESP
    para dar respuesta a las peticiones del maestro sd
    """
    master_data = request.POST # donde se encuentran las peticiones del maestro
    #bases de datos que se consultan de acuerdo a las peticiones del maestro
    device = DeviceDescriptor.objects.filter(serial_Number=master_data["serial_Number"]).filter(ruleset_Ids=master_data["ruleset_Ids"]).filter(model_Id=master_data["model_Id"])
    # print(device)
    
    if len(device)==1:
        device = device[0]
        # print(device.geolocation.pk)
        #consulta de los canales ocupados por regiones
        spectrum = Spectrum.objects.filter(geolocation=device.geolocation.pk)
        ocuppied_channels = [] #lista de los canales ocupados
        for data in spectrum:
            start_freq = Frequency.objects.get(pk=data.channels.pk)
            ocuppied_channels.append(start_freq.frequency)
        #consulta de todos los canales para seleccionar los canales libres
        all_channels = Frequency.objects.all()
        all_channels = all_channels.values("frequency")
        all_channels = list(map(lambda table: table["frequency"], all_channels))
        #comparacion de canales para extraer los canales libres
        free_channels = []
        for i in all_channels:
            if i in ocuppied_channels:
                pass
            else:
                free_channels.append(i)
    else:
        print("informacion repetida o inexistente")

    #base de datos del espectro consultada y filtrada de acuerdo a la informacion
    #georeferenciada del maestro

    #formacion de la respuesta AVAIL_SPECTRUM_RESP
    avail_spectrum_resp = {"serial_Number": device.serial_Number,
                        "manufacturer_Id":device.manufacturer_Id,
                        "model_Id": device.model_Id, "ruleset_Ids": device.ruleset_Ids,
                        "free_spectra":free_channels,
                        }
    return JsonResponse(avail_spectrum_resp)

@csrf_exempt
def spectrum_use_resp(request):
    msg_master = request.POST
    # validacion de la existencia del dispositivo
    device = DeviceDescriptor.objects.filter(serial_Number=msg_master["serial_Number"]).filter(ruleset_Ids=msg_master["ruleset_Ids"]).filter(model_Id=msg_master["model_Id"]).count()
    if device == 1 :
        # informacion relacionada con el espectro
        spectra_use = float(msg_master["spectra_use"])
        frequency = Frequency.objects.filter(frequency=spectra_use)
        frequency = frequency.values("channels", "frequency")
        if len(frequency)==1:
            frequency = frequency[0]
            channels = frequency["channels"]
            last_pk = Spectrum.objects.all().latest('pk')
            spectrum = Spectrum.objects.create(pk=last_pk.id+1, operation=msg_master["operation"], channels_id= channels, geolocation_id=msg_master["dane_code"])
            msg_to_master = {"info": "information ok"}
        else:
            msg_to_master = {"info": "not valid information"}
    else:
        msg_to_master = {"info": "not valid information"}
    return JsonResponse(msg_to_master)
    
@csrf_exempt
def delete_channel_paws(request):
    msg_from_master = request.POST
    pk_channel = Frequency.objects.filter(frequency=msg_from_master["freq_used"])
    pk_channel = pk_channel[0].pk
    spectrum = Spectrum.objects.filter(channels=pk_channel).filter(geolocation=msg_from_master["dane_code"])
    if len(spectrum)==1:
        spectrum.delete()
    return JsonResponse({"delete": "delete ok"})

