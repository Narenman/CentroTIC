import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import requests
import json

class Analogico():
    """ Esta clase se encarga de administrar el sensado analogico, es decir,
    en extraer los datos de la nariz electronica y de los sensores de agua.

    El sensado se realiza con un MCP3008 que se conecta a la raspberry pi3 
    mediante protocolo SPI del MCP3008, la conexion se realiza de la siguiente
    forma:

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
    """
    def __init__(self, direccionIP):
        self.direccionIP = direccionIP
    
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
        #sensores conectados al ADC1
        MQ2 = adc1[0]
        MQ3 = adc1[1]
        MQ4 = adc1[3]
        MQ5 = adc1[4]
        PH = adc1[6]
        turb = adc1[7]
        #sensores conectados al ADC2
        MQ135 = adc2[2]
        MQ6 = adc2[3]
        MQ7 = adc2[4]
        MQ8 = adc2[5]
        MQ9 = adc2[6]
        MICS5524 = adc2[7]
        agua = [PH, turb]
        aire = [MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ9, MQ135, MICS5524]
        return agua, aire
    
    def comunicacionAPI(self, URL,valor, ubicacion):
        """ este metodo es para comunicarse con la base 
        de datos a traves de API REST
        """
        data = {"valor": valor,
                "kit_monitoreo": 1,
                "ubicacion": ubicacion}
        headers={"Authorization":"Token 33565da4cc7e8394310dfa74160222e484b4fe6f"} 
        r = requests.post(URL, data=data, headers=headers)
        if r.status_code==200 or r.status_code==201:
            print("HTTP status ok. {}".format(r.status_code))
            r.close()
        else:
            print("Bad request {}".format(r.status_code))
    
    #estas se ejecutaran en el suscriptor MQTT
    def phAgua(self, ubicacion):
        agua, aire = self.sensores()
        ph = agua[0]
        URL = "http://"+self.direccionIP+"/app_praes/ph-agua/"
        self.comunicacionAPI(URL, ph, ubicacion)
    
    def turbidezAgua(self, ubicacion):
        agua, aire = self.sensores()
        turb = agua[1]
        URL = "http://"+self.direccionIP+"/app_praes/turbidez-agua/"
        self.comunicacionAPI(URL, turb, ubicacion)
    
    def calidadAire(self, ubicacion):
        agua, aire = self.sensores()
        URL = "http://"+self.direccionIP+"/app_praes/modo-nariz/"
        data = {"valor": json.dumps(aire),
                "kit_monitoreo": 1,
                "ubicacion": ubicacion}
        headers={"Authorization":"Token 33565da4cc7e8394310dfa74160222e484b4fe6f"} 
        r = requests.post(URL, data=data, headers=headers)
        if r.status_code==200 or r.status_code==201:
            print("HTTP status ok. {}".format(r.status_code))
            r.close()
        else:
            print("Bad request {}".format(r.status_code))

if __name__ == "__main__":
    direccionIP = "192.168.0.103:8000"
    lecturas = Analogico(direccionIP)
    print(lecturas.sensores())
    for i in range(20):
        # lecturas.phAgua(1)
        # lecturas.turbidezAgua(1)
        lecturas.calidadAire(1)
        time.sleep(2)