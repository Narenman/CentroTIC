import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import adafruit_sgp30
import board
import busio
import bme280

import time
import requests
import json

import os
import glob
import time
import sys



class AnalogicoDigital():
    """ Esta clase se encarga de administrar el sensado analogico, es decir,
    en extraer los datos de la nariz electronica y de los sensores de agua.

    El sensado se realiza con un MCP3008 que se conecta a la raspberry pi3 
    mediante protocolo SPI del MCP3008, la conexion se realiza de la siguiente
    forma, los ADC se conectan a 5V

    1) pines utilizados hardware SPI
    GPIO     MCP3008
    11       CLK
    9        DOUT
    10       DIN
    8        CS  

    2) pines utilizados software SPI
    GPIO     MCP3008
    18       CLK
    23       DOUT
    24       DIN
    25       CS

    Esta clase tambien realiza lectura del sensor de gas
    digital sgp30 mediante la conexion a los siguientes pines, 
    los sensores se conectan a 3.3V

    GPIO    SGP30   BME280
    2       SDA     SDA
    3       SCL     SCL

    Realiza lectura al sensor de flujo YFS201

    GPIO BOARD
    33
    """
    def __init__(self, direccionIP, APIusername, APIpassword):
        self.direccionIP = direccionIP
        self.APIusername = APIusername
        self.APIpassword = APIpassword

    def leer_temperatura(self):
        #sensor de temperatura agua
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        _direccion = '/sys/bus/w1/devices/'
        dispositivo_folder = glob.glob(_direccion + '28*')[0]
        dispositivo_pad = dispositivo_folder + '/w1_slave'
        f = open(dispositivo_pad, 'r')
        lineas = f.readlines()
        f.close()
        return lineas
    
    def determinar_valores(self):
        lineas = self.leer_temperatura()
        while lineas[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lineas = self.leer_temperatura()
        igual_pos = lineas[1].find('t=')
        if igual_pos != -1:
            temp_string = lineas[1][igual_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f
    
    def sgp30(self):
        """Esta funcion se encarga de realizar las lecturas del sensor
        digital sgp30 para mirar la calidad del aire """
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)       
        # Create library object on our I2C port
        sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)      
        # print("SGP30 serial #", [hex(i) for i in sgp30.serial])       
        sgp30.iaq_init()
        sgp30.set_iaq_baseline(0x8973, 0x8aae)
        eC02 = sgp30.eCO2 #ppm
        tvoc = sgp30.TVOC #ppb
        return eC02, tvoc
    
    def bme280x(self):
        """Se encarga de realizar las lecturas del sensor digital
        bme280 para medir variables temperatura, humedad y presion """
        temperature,pressure,humidity = bme280.readBME280All()
        return temperature, pressure, humidity

    
    def leerADC(self):
        """Activa los SPI de los MCP3008 """
        #ADC1 hardware SPI configuration
        SPI_PORT   = 0
        SPI_DEVICE = 0
        mcp1 = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

        #ADC2 Software SPI configuration:
        CLK  = 18   #CLK
        MISO = 23   #DOUT
        MOSI = 24   #DIN
        CS   = 25   #CS
        mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

        #vector de los ocho canales por ADC
        adc1 = [0]*8
        adc2 = [0]*8

        for i in range(8):
            adc1[i] = mcp1.read_adc(i)*5/1023.0
            adc2[i] = mcp2.read_adc(i)*5/1023.0 
        return adc1, adc2
    
    def sensores(self):
        """Esta funcion se encarga de organizar los sensores de acuerdo 
        a la conexion hardware para tener una mejor identificacion con 
        el software """
        adc1, adc2 = self.leerADC()
        eC02, tvoc = self.sgp30()
        #sensores conectados al ADC1
        MQ2 = adc1[0]
        MQ3 = adc1[1]
        MQ4 = adc1[3]
        MQ5 = adc1[4]
        PH = adc1[6]
        turb = adc1[7]
        #sensores conectados al ADC2
        MICS5524 = adc2[0]
        MQ8 = adc2[1]
        MQ135 = adc2[2]
        MQ6 = adc2[3]
        MQ7 = adc2[4]
        MQ9 = adc2[6]
        agua = [PH, turb]
        aire = [MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ9, MQ135, MICS5524, eC02, tvoc]
        return agua, aire

    #comunicacion con la API
    def getToken(self, username, password):
        """Esta funcion se encarga de consultar el token de acuerdo al usuario
        y contrasena para la API """
        data = {
        "username": username,
        "password": password}
        URL = "http://"+self.direccionIP+"/app_praes/token/"
        r = requests.post(URL, data=data)
        print("HTTP status token {}".format(r.status_code))
        token = json.loads(r.content)
        # print(token["token"])
        return token
    
    def comunicacionAPI(self, URL,valor, ubicacion, kit):
        """ este metodo es para comunicarse con la base 
        de datos a traves de API REST
        """
        data = {"valor": valor,
                "kit_monitoreo": kit,
                "ubicacion": ubicacion}
        token = self.getToken(self.APIusername, self.APIpassword)
        headers={"Authorization":"Token "+token["token"]} 
        r = requests.post(URL, data=data, headers=headers)
        if r.status_code==200 or r.status_code==201:
            print("HTTP status API. {}".format(r.status_code))
            r.close()
        else:
            print("Bad request {}".format(r.status_code))
    
    #sensores de AGUA
    def phAgua(self, ubicacion, kit):
        agua, aire = self.sensores()
        ph = agua[0]
        print("PH {}".format(ph))

        URL = "http://"+self.direccionIP+"/app_praes/ph-agua/"
        self.comunicacionAPI(URL, ph, ubicacion, kit)
    
    def turbidezAgua(self, ubicacion, kit):
        agua, aire = self.sensores()
        turb = agua[1]
        print("turbidez {}".format(turb))
        URL = "http://"+self.direccionIP+"/app_praes/turbidez-agua/"
        self.comunicacionAPI(URL, turb, ubicacion, kit)

    def tempeAgua(self, ubicacion, kit):
        tem_c, tem_f = self.determinar_valores()
        URL = "http://"+self.direccionIP+"/app_praes/temperatura-agua/"
        self.comunicacionAPI(URL, tem_c, ubicacion, kit)
    
    #calidad del aire
    def calidadAire(self, ubicacion, kit):
        agua, aire = self.sensores()
        print("aire".format(aire))
        URL = "http://"+self.direccionIP+"/app_praes/modo-nariz/"
        data = {"valor": json.dumps(aire),
                "kit_monitoreo": kit,
                "ubicacion": ubicacion}
        token = self.getToken(self.APIusername, self.APIpassword)
        headers={"Authorization":"Token "+token["token"]} 
        r = requests.post(URL, data=data, headers=headers)
        if r.status_code==200 or r.status_code==201:
            print("HTTP status API. {}".format(r.status_code))
            # print("aire {}".format(aire))
            r.close()
        else:
            print("Bad request {}".format(r.status_code))
    
    #variables del clima
    def climaTemperatura(self,ubicacion, kit):
        temperatura, presion, humedad = self.bme280x()
        URL = "http://"+self.direccionIP+"/app_praes/temperatura/"
        self.comunicacionAPI(URL, temperatura,ubicacion,kit)    

    def climaHumedad(self, ubicacion, kit):
        temperatura, presion, humedad = self.bme280x()
        URL = "http://"+self.direccionIP+"/app_praes/humedad/"
        self.comunicacionAPI(URL, humedad, ubicacion,kit)
    
    def climaPresion(self, ubicacion, kit):
        temperatura, presion, humedad = self.bme280x()
        URL = "http://"+self.direccionIP+"/app_praes/presion-atmosferica/"
        self.comunicacionAPI(URL, presion,ubicacion,kit)

    def flujo_agua(self):
        GPIO.setmode(GPIO.BCM)
        # inpt = 33 #BOARD
        inpt = 13
        GPIO.setup(inpt,GPIO.IN)
        constante = 0.10
        time_new = time.time() + 1
        rate_cnt = 0
        while time.time() <= time_new:
            try:
                if GPIO.input(inpt)!=0:
                    rate_cnt +=1
            except:
                print('\nCTRL C - Exiting nicely')
                GPIO.cleanup()
                sys.exit()
        print('\nLiters / min ', round(rate_cnt*constante,4))
        GPIO.cleanup()
        return rate_cnt*constante

    def flujo_agua_API(self, ubicacion, kit):
        valor = self.flujo_agua()
        URL = "http://"+self.direccionIP+"/app_praes/flujo-agua"
        self.comunicacionAPI(URL, valor, ubicacion, kit)

if __name__ == "__main__":
    #parametros de configuracion
    direccionIP = "192.168.0.102:8000"
    APIusername = "mario"
    APIpassword = "mario"

    lecturas = AnalogicoDigital(direccionIP, APIusername, APIpassword)
    kit = 1
    ubicacion = 43
    # print("temperatura", lecturas.determinar_valores())
    for i in range(20):
        lecturas.phAgua(ubicacion, kit)
        lecturas.turbidezAgua(ubicacion, kit)
        lecturas.calidadAire(ubicacion, kit)
        lecturas.flujo_agua()
        time.sleep(2)