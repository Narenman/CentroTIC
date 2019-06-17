from django.shortcuts import render
import re
import json
import time
from django.contrib.auth.decorators import login_required
from .forms import UsuariosPrimariosForm
from .models import UsuariosPrimarios

# Create your views here.

def index(request):
    respuesta = {}
    return render(request, "bloqueadores/index.html", respuesta)


@login_required
def jamming(request):
    """Para hacer bloqueo manual del espectro"""

    dict1 = dict()
    username = "pi"
    password = "raspberry"
    MQTT_broker = "34.74.6.16"

    MQTT_port = 1883
    K  = 10 # number of average
    L  = 4096 # fft size,
    N  = 10 # frames of samples
    ins = request.POST
    N_keys = ins.keys()
    N_USRPS = re.findall(r'USRP\w',''.join(N_keys))
    print(ins)

    try:
        freq = float(ins['freq'])
        SCAN_REQ = json.dumps({"Center Freq":freq*1000000, "sample_rate": 250000, "Antenna": "RX", "flag":"0", "freq_list":[]})
        # objMQTT = MQTT_Master_assist.MQTTmanagerServer(username, password, MQTT_broker, MQTT_port, INIT_REQ, SCAN_REQ, N_USRPS, N, K, L)
        dict1 = {'orden':[],'N_USRPS': N_USRPS}
        if (('USRP1' in N_keys) or ('USRP2' in N_keys) or ('USRP3' in N_keys)) and (freq >= 88.0 and freq < 108):
            # objMQTT.pub_messages_to_devices(INIT_REQ)
            # msgs_USRPS = objMQTT.sub_init_com()
            # time.sleep(3)
            # objMQTT.pub_messages_to_devices(SCAN_REQ)
            del(dict1['orden'])
            ins = request.POST
            print("\nbloqueando")
        else:
            dict1 = {'orden':'Por favor seleccione al menos un USRP y la frecuencia entre 88-108 MHz'}
        # del(objMQTT)
    except KeyError:
            dict1 = {'orden': 'Ningun elemento seleccionado'}
    except ValueError:
            freq = 0.0
            dict1 = {'orden': 'Por favor ingrese la frecuencia entre 88 y 108 MHz'}
    return render(request, 'bloqueadores/jamming.html',dict1)


@login_required
def monitoring(request):
    """ Para hacer monitoreo del espectro """    
    USRPS = request.GET
    cont = dict()
    ##################  MQTT  ##############33
    username = "pi"
    password = "raspberry"
    MQTT_broker = "34.74.6.16"
    MQTT_port = 1883

    # informacion para enviar al USRP
    K  = 10 # number of average
    L  = 4096 # fft size,
    N  = 25 # frames of samples
    fs = 16e6
    f_mixer = [96e6, 112e6]

    # INIT_REQ = json.dumps({"deviceDesc":["server", "django", "0x12345"], "frames": N, "K": K, "fft size": L, 'flag':"exit"}); #content type protocol
    # SCAN_REQ = json.dumps({"Center Freq":112e6, "sample_rate": 16000000, "Antenna": "RX", "flag":"1", 'freq_list':[]})
    N_keys = USRPS.keys()
    print(N_keys)
    N_USRPS = re.findall(r'USRP\w',''.join(N_keys))
    cont.update(USRPS)
    print(N_USRPS)
    if ("USRP1" in N_keys or "USRP2" in N_keys or "USRP3" in N_keys) and USRPS["escanear"]=="escanear" and 'metodo' in N_keys:
        print("joder")
    
    return render(request, "bloqueadores/monitoring.html", cont)

def consulta_usuarios_primarios(request):
    usuarios_primarios = UsuariosPrimariosForm()
    if request.POST:
        dato_cliente = request.POST
        print(dato_cliente["ciudad"])
        usuarios = UsuariosPrimarios.objects.filter(ciudad_id=dato_cliente["ciudad"])
        usuarios = usuarios.values("nombre_emisora", "clase_emisora", "frecuencia")
        respuesta = {"usuarios_primarios": usuarios_primarios, "usuarios": usuarios}
        print(usuarios)
    else:
        respuesta = {"usuarios_primarios": usuarios_primarios}
    return render(request, "bloqueadores/consulta_usuarios_primarios.html", respuesta)