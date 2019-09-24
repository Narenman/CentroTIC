import paho.mqtt.publish as publish
import json
import numpy
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3
from django.core import serializers

from .models import AlbumImagenes, Espectro, Estado, CaracteristicasAntena, \
                    CaracteristicasEstacion, RBW, CaracteristicasEspectro, RegionCampana, \
                        PosicionAntena, Servicios, Bandas, EstacionAmbiental
from .forms import EspectroForm, RFIForm, RegionForm

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder

# funciones auxiliares
def publishMQTT(topico, msg):
    """ Se encarga de establecer comunicacion
    MQTT con los dispositivos """
    IP_broker = "35.243.199.245"
    usuario_broker = "pi"
    password_broker = "raspberry"
    publish.single(topico, msg, port=1883, hostname=IP_broker,
     auth={"username": usuario_broker, "password":password_broker})

def promedio(espectro, nfft):
    """ Realiza promedios del espectro,
    debido a que las muestras estan almacenadas en un vector de tamano N
    que se subdivide N/nfft veces y ese es el numero que se promedia (K)"""
    K = int(len(espectro)/(nfft))
    x = numpy.zeros(nfft)
    for i in range(K):
        x = x + espectro[i*nfft:(i+1)*nfft]
    x = x/K
    return x

def ordenar_listas(lista):
    """Es para ordenar las listas que se envian a javascript para
    que highcharts realize las graficas, tiene la forma
    lista = [[98, -50], [99, -51],...]
    dos columnas frecuencia y espectro """
    df = pd.DataFrame(data=lista, columns=["frec", "espectro"])
    df = df.sort_values(by=["frec"])
    y = []
    for index, row in df.iterrows():
        y.append([row["frec"], row["espectro"]])
    return y

def detener(request):
    # cliente = request.POST
    # print(cliente)
    # stop = cliente["stop"]
    # topico = "radioastronomia/RFI"
    # msg = {"accion": stop}
    # publishMQTT(topico, json.dumps(msg))
    # return render(request, "radioastronomia/control_manual.html", {})

    """ Es para mostrar la interfaz del control manual del espectro """
    form = RegionForm()
    antena = CaracteristicasAntena.objects.all()
    antena = antena.values("id","referencia")     
    respuesta = dict()
    try:
        album = AlbumImagenes.objects.last()
        album = album.imagen
        if request.POST:
            print(request.POST)
            cliente = request.POST
            #preparacion de los mensajes para enviar a los dispositivos
            stop = cliente["stop"]
            msg = {"accion": stop}
            topico = "radioastronomia/RFI"
            #envio de la instruccion al subsistema RFI
            publishMQTT(topico, json.dumps(msg))
            respuesta.update({"imagenes": album, "form": form, "antenna": antena})
        else:
            respuesta.update({"imagenes": album, "form": form, "antenna": antena})
    except:
        form = RegionForm()   
        respuesta = {"form": form, "antenna": antena}             
    return render(request, "radioastronomia/control_manual.html", respuesta)

##############################################################
def analisis_tiempo(request):
    """Este es el modo 2 de analisis de datos para realizar 
    un estudio del tiempo por banda """
    bandas = Espectro.objects.distinct("frec_central")
    bandas = bandas.values("frec_central")
    frec_central = list(map(lambda x: x["frec_central"]/1e6, bandas))
    bandas = Espectro.objects.distinct("frec_muestreo")
    bandas = bandas.values("frec_muestreo")
    frec_muestreo  = list(map(lambda x: x["frec_muestreo"]/1e3, bandas))
    bandas = Espectro.objects.distinct("nfft")
    bandas = bandas.values("nfft")
    region = RegionCampana.objects.all()
    region = region.values("id", "zona")
    respuesta = {"bandas":frec_central,
                 "frecmuestreo": frec_muestreo,
                 "nfft": bandas, "region":region}
    if request.POST:
        cliente = request.POST
        print(cliente)
        nfft = int(cliente["nfft"])
        frec_central = int(float(cliente["bandas"])*1e6)
        frec_muestreo = int(float(cliente["frecmuestreo"])*1e3)
        region = cliente["region"]
        #consulta de la banda seleccionada
        #aca hago la clasificacion para crear el reporte
        print((frec_central-frec_muestreo/2)/1e6)
        print((frec_central+frec_muestreo/2)/1e6)
        servicios = Servicios.objects.filter(frecuencia_inicial__gte=(frec_central-frec_muestreo/2)/1e6)
        servicios = servicios.values("servicio", "frecuencia_inicial", "frecuencia_final")
        cnabf = []
        for ser in servicios:
            cnabf.append(ser)
            if ser["frecuencia_final"]>=(frec_central+frec_muestreo/2)/1e6:
                break
        print(cnabf)

        services = json.dumps(cnabf, cls=DjangoJSONEncoder)
        max_col     = max([len(m['servicio'].split('-')) for m in json.loads(services)])
        boxWidth    = len(cnabf)*160*2
        boxHeight   = max_col*(50+1)
        canvaSize   = {"Width": boxWidth,
                       "Height": boxHeight}

        # consulta del espectro
        espectro = Espectro.objects.filter(region=region).filter(frec_central=frec_central).filter(frec_muestreo=frec_muestreo).filter(nfft=nfft).filter(fecha__range=[cliente["fechaini"], cliente["fechafin"]])
        espectro = espectro.values("fecha", "espectro")
        #creacion del espectrograma
        char_ener = []
        tiempo = []
        frecuencia = []
        date = []
        espec = []

        if len(espectro)!=0:
            for esp in espectro:
                X = esp["espectro"]
                fecha = esp["fecha"]
                X = numpy.asarray(X)
                #promedio de los espectros por cada tiempo escogido
                X = promedio(espectro=X, nfft=nfft)
                char_ener.append(numpy.sum(10**(X/10)))
                #variables espectrograma
                tiempo.append(fecha.strftime('%m-%d %H:%M:%S'))
                f = numpy.arange(-int(nfft/2),int(nfft/2),1)*frec_muestreo/(nfft*2) + frec_central

                for i in range(nfft):
                    frecuencia.append(f[i]/1e6)
                    date.append(fecha.strftime('%m-%d %H:%M:%S'))
                    espec.append(X[i])

            df = pd.DataFrame(data={"Frecuencia":frecuencia, "Tiempo":date, "espectro": espec})
            df = df.pivot("Tiempo", "Frecuencia", "espectro")
            # espacio para la grafica del espectrograma

            fig, ax = plt.subplots()
            sns.distplot(10*numpy.log10(char_ener), kde_kws={"color": "k", "lw": 3, "label": "KDE"},
                hist_kws={"lw": 3, "label": "Histograma"}, ax=ax)
            ax.set(xlabel='Energia dBm', ylabel='',
            title='Histograma del comportamiento de la energia')
            ax.grid()
            histograma = mpld3.fig_to_html(fig)

            fig1, ax1 = plt.subplots()
            ax1.plot(tiempo, 10*numpy.log10(char_ener))
            ax1.set(xlabel="Tiempo DD H:M:s", ylabel="Energia dBm", title="Energia banda en funcion del tiempo")
            ax1.grid()
            tiempo_energia = mpld3.fig_to_html(fig1)

            fig2, ax2 = plt.subplots()
            sns.heatmap(df, yticklabels=5, xticklabels=120, cmap="coolwarm", ax=ax2)
            ax2.set(xlabel="Frecuencia MHz", ylabel="Tiempo", title="Espectrograma")
            ax2.grid()
            espectrograma = mpld3.fig_to_html(fig2)

            respuesta.update({"grafica": histograma, "enetiempo":tiempo_energia,
                            "espectrograma": espectrograma,
                            "frec_central": frec_central/1e6,
                            "frec_muestreo": frec_muestreo,
                            "services": services, 
                            "canvaSize": canvaSize})
    return render(request,"radioastronomia/analisis_tiempo.html", respuesta)


def bandas_espectrales(request):
    """Este es el modo 1 de analisis de datos para barrer todas las bandas
    espectrales"""
    region = RegionForm()
    rbw = RBW.objects.all().distinct("rbw") #para obtener los RBW disponibles
    respuesta = {"region": region, "rbw":rbw}
    return render(request, "radioastronomia/bandas_espectrales.html",respuesta)

def analisis_angular(request):
    bandas = Espectro.objects.all().distinct("frec_central")
    bandas = bandas.values("frec_central")
    bandas = list(map(lambda bandas:bandas["frec_central"]/1e6,bandas))
    region = RegionForm()
    rbw = RBW.objects.all().distinct("rbw")
    posicion = PosicionAntena.objects.all().distinct("azimut")
    elevacion = PosicionAntena.objects.all().distinct("elevacion")
    respuesta = {"bandas": bandas,
                 "region": region,
                 "rbw": rbw,
                 "azimut": posicion,
                 "elevacion": elevacion}
    return render(request, "radioastronomia/analisis_angular.html", respuesta)

#modo 3 de operacion
@csrf_exempt
def espectro_angulos(request):
    """Se encarga de  filtrar los querys teniendo en cuenta
    la fecha, la hora, minuto y segundo en que coinciden las mediciones
    """
    respuesta = dict()
    if request.POST:
        cliente = request.POST
        print(cliente)
        if "azimut" in cliente.keys():
            #variables de entrada
            azimut = float(cliente["azimut"])
            frec_central = int(float(cliente["bandas"])*1e6)
            inidate = cliente["fechaini"]
            enddate = cliente["fechafin"]
            region_id = int(cliente["region"])
            rbw = RBW.objects.get(rbw=float(cliente["RBW"]))
            nfft = rbw.nfft
            frec_muestreo = rbw.frecuencia_muestreo

            cursor = connection.cursor() #conexion a la base de datos
            #personalizacion del query
            query = []
            query.append("SELECT radioastronomia_espectro.espectro, radioastronomia_espectro.frec_central, radioastronomia_posicionantena.elevacion, radioastronomia_espectro.fecha ")
            query.append("FROM radioastronomia_espectro ")
            query.append("INNER JOIN radioastronomia_posicionantena ")
            query.append("ON date_trunc('second',radioastronomia_espectro.fecha)=date_trunc('second',radioastronomia_posicionantena.fecha) ")
            query.append("WHERE radioastronomia_posicionantena.azimut= %s ")
            query.append("AND radioastronomia_espectro.frec_central=%s ")
            query.append("AND radioastronomia_espectro.frec_muestreo = %s ")
            query.append("AND radioastronomia_espectro.nfft = %s ")
            query.append("AND radioastronomia_espectro.region_id = %s ")
            query.append("AND date_trunc('day', radioastronomia_espectro.fecha)>= to_date(%s, 'YYYY-MM-DD') ")
            query.append("AND date_trunc('day', radioastronomia_espectro.fecha)<=to_date(%s, 'YYYY-MM-DD') ")
            query.append("ORDER BY radioastronomia_posicionantena.elevacion;")
            query = "".join(query)

            cursor.execute(query,[azimut, frec_central, frec_muestreo, nfft, region_id, inidate, enddate])
            rows = cursor.fetchall()
            
            ele = []
            ener = []
            for row in rows:
                espectro = row[0]
                elevacion = row[2]
                espectro = promedio(espectro, nfft)
                ener.append(numpy.sum(10**(espectro/10)))
                ele.append(elevacion)
            angular = {"elevacion": ele, "energia": ener}
            df = pd.DataFrame(data=angular)
            df = df.groupby("elevacion")
            dfm = df.mean()
            print(dfm)
            elevacion = dfm.index.tolist()
            elevacion = numpy.asarray(elevacion)
            # elevacion = elevacion*numpy.pi/180
            energia = dfm["energia"].tolist()
            energia = numpy.asarray(energia)
            energia = 1000*energia
            # energia = 10*numpy.log10(energia)

            #datos para javascript
            angular = list(map(lambda elevacion, energia: [elevacion, energia], elevacion, energia))
            respuesta.update({"pos":"elevacion"})
            
        elif "elevacion" in cliente.keys():
            #variables de entrada
            elevacion = float(cliente["elevacion"])
            frec_central = int(float(cliente["bandas"])*1e6)
            inidate = cliente["fechaini"]
            enddate = cliente["fechafin"]
            rbw = RBW.objects.get(rbw=float(cliente["RBW"]))
            nfft = rbw.nfft
            frec_muestreo = rbw.frecuencia_muestreo
            region_id = int(cliente["region"])


            cursor = connection.cursor() #conexion a la base de datos
            #personalizacion del query
            query = []
            query.append("SELECT radioastronomia_espectro.espectro, radioastronomia_espectro.frec_central, radioastronomia_posicionantena.azimut, radioastronomia_espectro.fecha ")
            query.append("FROM radioastronomia_espectro ")
            query.append("INNER JOIN radioastronomia_posicionantena ")
            query.append("ON date_trunc('second',radioastronomia_espectro.fecha)=date_trunc('second',radioastronomia_posicionantena.fecha) ")
            query.append("WHERE radioastronomia_posicionantena.elevacion= %s ")
            query.append("AND radioastronomia_espectro.frec_central=%s ")
            query.append("AND radioastronomia_espectro.frec_muestreo = %s ")
            query.append("AND radioastronomia_espectro.nfft = %s ")
            query.append("AND radioastronomia_espectro.region_id = %s ")
            query.append("AND date_trunc('day', radioastronomia_espectro.fecha)>= to_date(%s, 'YYYY-MM-DD') ")
            query.append("AND date_trunc('day', radioastronomia_espectro.fecha)<=to_date(%s, 'YYYY-MM-DD') ")
            query.append("ORDER BY radioastronomia_posicionantena.azimut;")
            query = "".join(query)

            cursor.execute(query,[elevacion, frec_central, frec_muestreo, nfft, region_id, inidate, enddate])
            rows = cursor.fetchall()
            
            ele = []
            ener = []
            for row in rows:
                espectro = row[0]
                elevacion = row[2]
                espectro = promedio(espectro, nfft)
                ener.append(numpy.sum(10**(espectro/10)))
                ele.append(elevacion)
            angular = {"elevacion": ele, "energia": ener}
            df = pd.DataFrame(data=angular)
            df = df.groupby("elevacion")
            dfm = df.mean()
            print(dfm)
            elevacion = dfm.index.tolist()
            elevacion = numpy.asarray(elevacion)
            # elevacion = elevacion*numpy.pi/180
            energia = dfm["energia"].tolist()
            energia = numpy.asarray(energia)
            energia = 1000*energia
            # energia = 10*numpy.log10(energia)

            #datos para javascript
            angular = list(map(lambda elevacion, energia: [elevacion, energia], elevacion, energia))
            respuesta.update({"pos":"azimut"})
    else:
        angular = []
    respuesta.update({"angular": angular})
    return JsonResponse(respuesta)

#modo 1 de operacion del espectro
@csrf_exempt
def barrido_json(request):
    respuesta = dict()
    if request.POST:
        # try:
        cliente = request.POST
        print(cliente)
        # analisis RF
        #obtener frecuencia de muestreo y nfft
        resBW = RBW.objects.get(rbw=cliente["RBW"])
        frec_muestreo = resBW.frecuencia_muestreo
        nfft = resBW.nfft
        #filtrado para obtener cada banda
        frec_central = Espectro.objects.filter(nfft=nfft).filter(frec_muestreo=frec_muestreo).filter(region=cliente["region"]).filter(fecha__range=[cliente["fechaini"], cliente["fechafin"]]).distinct("frec_central")
        frec_central = frec_central.values("frec_central")
        #ahora se obtiene el espectro por cada banda espectral
        y = numpy.array([])
        freq = []
        fechas = []
        char_energia = []
        freq_prueba = numpy.array([])
        for f in frec_central:
            rows = Espectro.objects.filter(nfft=nfft).filter(frec_muestreo=frec_muestreo).filter(frec_central__exact=f["frec_central"]).order_by("frec_central")
            rows = rows.values("fecha", "espectro")
            x_ = numpy.zeros(nfft)
            #este ciclo promedia todos los espectros asociados a la banda
            for row in rows:
                espectro = row["espectro"]
                espectro = numpy.asarray(espectro)
                x = promedio(espectro, nfft)
                x_ = x_ + x
                fechas.append(row["fecha"])
            x_ = x_/len(rows)    
            y = numpy.append(y, x_)
            freq_prueba = numpy.append(freq_prueba, numpy.arange(-int(nfft/2),int(nfft/2),1)*frec_muestreo/(nfft*2) + f["frec_central"]) 
            
            freq.append(f["frec_central"])
            #analsis caracteristicas de la energia
            ids = Espectro.objects.filter(frec_central=f["frec_central"])
            ids = ids.values("id")
            car_energia =CaracteristicasEspectro.objects.filter(espectro__in=ids)
            car_energia = car_energia.values("energia")
            
            mu = 0
            for row in car_energia:
                energia = row["energia"]
                energia = numpy.asarray(energia)
                mu = mu + numpy.mean(energia)
            mu = mu/len(car_energia)
            mu = 10*numpy.log10(mu)
            char_energia.append(mu)

        #organizacion de los datos para las graficas
        data_energia = []
        for i in range(len(freq)):
            data_energia.append([freq[i]/1000000, char_energia[i]])

        data = []
        for j in range(len(freq_prueba)):
            data.append([freq_prueba[j]/1000000.0, y[j]])
        
        #ordena los datos del espectro por frecuencia para mejor visualizacion
        data = ordenar_listas(data)
        
        respuesta.update({"datos": len(y), "lenf": len(freq),
                            "data": data, "data_energia": data_energia,
                            "frec_muestreo": frec_muestreo,
                            "nfft": nfft})
    return JsonResponse(respuesta)


def json_estacion(request):
    respuesta = dict()

    estacion = EstacionAmbiental.objects.last()
    respuesta.update({"temp": estacion.temperatura,
                "hum": estacion.humedad_relativa,
                "pres": estacion.presion_atomosferica,
                "rad": estacion.radiacion_solar,
                "vel_vien": estacion.vel_viento,
                "dir_vien": estacion.dir_viento,
                "pres": estacion.precipitacion})
    return JsonResponse(respuesta)

def json_spectro(request):
    """Se encarga retornar los valores que muestra el espectro
    en el navegador para el modo manual"""
    try:
        espectro = Espectro.objects.last()
        nfft = espectro.nfft
        frec_central = espectro.frec_central
        frec_muestreo = espectro.frec_muestreo
        print(frec_muestreo)
        espectro = espectro.espectro
        espectro = numpy.asarray(espectro)
        # promediado del espectro
        K = int(len(espectro)*2/(nfft*3))
        print(K, "K")
        x = numpy.zeros(nfft)
        for i in range(K):
            x = x + espectro[i*nfft:(i+1)*nfft]
        x = x/K
        frec = (numpy.arange(-int(nfft/2),int(nfft/2),1)*frec_muestreo/nfft + frec_central)/1e6 #puntos espectrales
        
        #organizacion de los datos para que javascript los pueda interpretar
        respuesta = []
        for i in range(nfft):
            respuesta.append([frec[i], x[i]])
    except:
        respuesta = {}
    return JsonResponse({"espectro":respuesta})

#modo 4 de operacion
def comparacion_zonas(request):

    regiones = RegionCampana.objects.all()
    regiones = regiones.values("id", "zona")
    ener = numpy.array([])
    media = numpy.array([])
    mediana = numpy.array([])
    std = numpy.array([])
    max_ = numpy.array([])
    min_ = numpy.array([])
    espectros = []

    columns = ["ener", "media", "mediana", "std", "max", "min"]
    target = []
    if request.POST:
        cliente = request.POST
        print(cliente)
        rbw = RBW.objects.get(rbw=cliente["RBW"])
        print(rbw)
        nfft = rbw.nfft
        samp_rate = rbw.frecuencia_muestreo
        fig1, ax1 = plt.subplots()
        for reg in regiones:
            frecuencias = Espectro.objects.filter(region=reg["id"]).values("frec_central").distinct().order_by("frec_central")
            y = numpy.array([])
            freq_ = numpy.array([])
            target.append(reg["id"])

            if len(frecuencias)>0:
                for freq in frecuencias[:3]:
                    print(freq)
                    espectro = Espectro.objects.filter(region=reg["id"]).values("espectro").filter(frec_central=freq["frec_central"]).filter(frec_muestreo=samp_rate).order_by("fecha")
                    print(len(espectro))
                    x_ = numpy.zeros(nfft)
                    for row in espectro:
                        x = numpy.asarray(row["espectro"])
                        x = promedio(x,nfft)
                        x_ = x_ + x
                    x_ = x_/len(espectro)
                    freq_ = numpy.append(freq_, numpy.arange(-int(nfft/2),int(nfft/2),1)*samp_rate/(nfft*2) + freq["frec_central"])
                    y = numpy.append(y,x_)
                
                freq_ = freq_/1e6 #escala de la frecuencia
                #analisis de caracteristicas

                ## aca van las graficas
                ax1.plot(freq_, y, label=reg["zona"])
                ax1.set(xlabel="Frecuencia MHz", ylabel="Espectro dBm", title="Espectro por region",)
                ax1.legend()
                ax1.grid(True)
                espectros = mpld3.fig_to_html(fig1)

                y = 10**(y/10)
                ener = numpy.append(ener,numpy.sum(y))
                media = numpy.append(media, numpy.mean(y))
                mediana = numpy.append(mediana, numpy.median(y))
                std = numpy.append(std, numpy.std(y))
                max_ = numpy.append(max_,numpy.max(y))
                min_ = numpy.append(min_, numpy.min(y))
            else:
                pass
        
        if len(ener)>1:
            #analisis caracteristicas
            X = numpy.vstack([ener, media, mediana, std, max_, min_])
            df = pd.DataFrame(data=X.T, columns=columns)
            print(df.head())
            #escalado de los datos
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            scaler.fit(df)
            scaled_data = scaler.transform(df)
            #aplicacion de PCA
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            pca.fit(scaled_data)
            x_pca = pca.transform(scaled_data)

            fig2, ax2 = plt.subplots()
            ax2.scatter(x_pca[:,0], x_pca[:,1], c=target, cmap="plasma")
            ax2.set(xlabel="pc1", ylabel="pc2", title="Zonas registradas")
            ax2.legend(title="Regiones")
            ax2.grid()
            caracteristicas = mpld3.fig_to_html(fig2)
        else:
            caracteristicas  = []

        rbw = RBW.objects.all()
        respuesta = {"espectros": espectros,
                    "caracteristicas": caracteristicas,
                    "rbws": rbw}
    else:
        rbw = RBW.objects.all()
        respuesta = {"rbws":rbw}
    return render(request, "radioastronomia/comparacion_zonas.html", respuesta)


@csrf_exempt
def control_manual(request):
    """ Es para mostrar la interfaz del control manual del espectro """
    form = RegionForm()
    antena = CaracteristicasAntena.objects.all()
    antena = antena.values("id","referencia")     
    respuesta = dict()
    try:
        album = AlbumImagenes.objects.last()
        album = album.imagen
        if request.POST:
            print(request.POST)
            cliente = request.POST
            rbw = RBW.objects.get(rbw=cliente["RBW"])
            nfft = rbw.nfft
            frecuencia_muestreo = rbw.frecuencia_muestreo
            #preparacion de los mensajes para enviar a los dispositivos
            msg = {"nfft": nfft, "sample_rate": frecuencia_muestreo,
            "ganancia": 50, "duracion": 5, "frec_central": int(float(cliente["frequency"])*1e6),
            "accion": "modo manual", "region": int(cliente["region"]), "elevacion":int(cliente["elevacion"]),
            "azimut":int(cliente["azimut"]), "antena":int(cliente["antena"])}
            topico = "radioastronomia/RFI"
            #envio de la instruccion al subsistema RFI
            publishMQTT(topico, json.dumps(msg))
            respuesta.update({"imagenes": album, "form": form, "antenna": antena})
        else:
            respuesta.update({"imagenes": album, "form": form, "antenna": antena})
    except:
        form = RegionForm()   
        respuesta = {"form": form, "antenna": antena}             
    return render(request, "radioastronomia/control_manual.html", respuesta)

@csrf_exempt
def control_automatico(request):
    form = RFIForm()
    respuesta = dict()
    antena = CaracteristicasAntena.objects.all()
    antena = antena.values("id","referencia")  

    if request.POST:
        cliente = request.POST
        print(cliente)
        rbw = RBW.objects.get(rbw=cliente["RBW"])
        nfft = rbw.nfft
        frecuencia_muestreo = rbw.frecuencia_muestreo
        msg = {"nfft": nfft, "sample_rate": frecuencia_muestreo,
        "ganancia": 50, "duracion": 2, "frecuencia_inicial": int(float(cliente["finicial"])*1e6),
        "accion": "modo automatico",
        "region": int(cliente["region"]), "frecuencia_final": int(float(cliente["ffinal"])*1e6),
        "azinicial": float(cliente["azinicial"]), "azfinal":float(cliente["azfinal"]),
        "eleninicial": float(cliente["eleninicial"]), "elefinal":float(cliente["elefinal"]),
        "antena":int(cliente["antena"]), "RBelevacion": float(cliente["RBelevacion"]), 
        "RBazimut":float(cliente["RBazimut"])}
        topico = "radioastronomia/RFI"
        # #envio de la instruccion al subsistema RFI
        publishMQTT(topico, json.dumps(msg))
    respuesta.update({"form": form, "antenna": antena})

    return render(request, "radioastronomia/control_automatico.html", respuesta)

# Informacion adicional de antenas utilizadas
class CaracteristicasAntenaListView(ListView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_list.html"
    context_object_name = "caracteristicasantena"

class CaracteristicasAntenaCreateView(CreateView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_create.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:antenas")

class CaracteristicasAntenaUpdateView(UpdateView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_update.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:antenas")

class CaracteristicasAntenaDeleteView(DeleteView):
    model = CaracteristicasAntena
    template_name = "radioastronomia/caracteristicasantena_delete.html"
    success_url = reverse_lazy("radioastronomia:antenas")
    context_object_name = "caracteristicasantena"

#informacion adicional de la estacion de monitoreo
class CaracteristicasEstacionListView(ListView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_list.html"
    context_object_name="caractestacion"

class CaracteristicasEstacionCreateView(CreateView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_create.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:subsistema-estacion")

class CaracteristicasEstacionUpdateView(UpdateView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_update.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:subsistema-estacion")

class CaracteristicasEstacionDeleteView(DeleteView):
    model = CaracteristicasEstacion
    template_name = "radioastronomia/caracteristicasestacion_delete.html"
    context_object_name = "caracterstacion"
    success_url = reverse_lazy("radioastronomia:subsistema-estacion")

## informacion sobre las resoluciones espectrales
class RBWListView(ListView):
    model = RBW
    template_name = "radioastronomia/rbw_list.html"
    context_object_name="rbw"

class RBWDeleteView(DeleteView):
    model = RBW
    template_name = "radioastronomia/rbw_delete.html"
    context_object_name = "rbw"
    success_url = reverse_lazy("radioastronomia:rbw")

def RBWcreate(request):
    if request.POST:
        cliente = request.POST
        frecuencia_muestreo = cliente["frec_muestreo"]
        nfft = cliente["nfft"]
        rbw = float(frecuencia_muestreo)/float(nfft)
        rbwmodel = RBW(frecuencia_muestreo=frecuencia_muestreo, nfft=nfft, rbw=rbw)
        rbwmodel.save()
        return HttpResponseRedirect(reverse_lazy("radioastronomia:rbw"))
    return render(request, "radioastronomia/rbw_create.html")

class RBWUpdateView(UpdateView):
    model = RBW
    template_name = "radioastronomia/rbw_update.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:rbw")

## informacion sobre los lugares de medicion
class RegionCampanaListView(ListView):
    model = RegionCampana
    template_name = "radioastronomia/index.html"
    context_object_name ="region"

class RegionCreateView(CreateView):
    model = RegionCampana
    template_name = "radioastronomia/region_create.html"
    fields = "__all__"
    success_url = reverse_lazy("radioastronomia:index")

def subsistemacielo(request):
    respuesta = dict()
    try:
        album = AlbumImagenes.objects.last()
        respuesta.update({"imagen": album.imagen,
                    "fecha": album.fecha,
                    "zona": album.region})
        if request.POST:
            print(request.POST)
    except:
        pass
    return render(request, "radioastronomia/subsistema_camara.html", respuesta)