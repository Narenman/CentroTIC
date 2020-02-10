import requests
import json
import serial
import time

""" este archivo contiene lo relacionado al RS232 y
adquisicion de datos por el rotor
"""

class YaetsuG5500():
    def __init__(self,IP):
        self.PORT     = '/dev/ttyUSB0'
        self.BAUDRATE = 9600
        self.BYTESIZE        = serial.EIGHTBITS
        self.PARITY          = serial.PARITY_NONE
        self.STOPBITS        = serial.STOPBITS_ONE
        self.gs232b = serial.Serial(self.PORT,
                                    self.BAUDRATE,
                                    self.BYTESIZE,
                                    self.PARITY,
                                    self.STOPBITS)

        self.gs232b.flush()
        self.S = True
        self.IP = IP
    
    def estadoposicion_put(self,activo, azimut, elevacion):
        """Actualiza la posicion actual del rotor en la base de datos """
        pyload = {"activo": activo,
                "azimut": azimut,
                "elevacion": elevacion} 
        url = "http://"+self.IP+"/radioastronomia/estado/posicion/1"          
        r = requests.put(url, data=pyload)
        print("HTTP status code {} actulizacion posicion PUT".format(r.status_code))
        r.close()

    def paracons(self, P):
        """ paracons(Al=90, EL=45) = [090,045] """
        ZP=""
        for i in range(1, 3-len(str(P))+1):
            ZP += "0"

        if ZP:
            return "{}{}".format(str(ZP), str(P))

        else:
            return str(P)

    def stop(self):
        print("Antena en posicion")
        self.gs232b.flush()
        self.gs232b.close()

    def consulta(self):
        """Consulta por el puerto serial la posicion del rotor """
        self.gs232b.write(b'C2\r')
        angles = str(self.gs232b.read(14))[1:]
        l=len(angles)
        self.gs232b.flushInput()

        angles = angles.replace("'","")
        angles = angles.split("  ")
        angles = [angles[0].split("=")[1], angles[1].split("=")[1]]
        return [angles[0], angles[1], l]

    def control(self, azimut, elevacion, region, antena):
        """se encarga de enviarle las instrucciones al YAETSU 5500 """

        print("enviando control\nazimut: {}\televacion: {}".format(azimut, elevacion))
        AZ = self.paracons(azimut)
        EL = self.paracons(elevacion)
        T = "W{} {}\r".format(AZ, EL)

        self.gs232b.write(T.encode())

        serial_angulos = self.consulta()
        print("Posicion Inicial", serial_angulos)
        activo = True
        azimut_s = serial_angulos[0]
        elevacion_s = serial_angulos[1]
        self.estadoposicion_put(activo, azimut_s, elevacion_s)

        while self.S:

            time.sleep(0.3)
            print(self.consulta())
            angles = self.consulta()
            varAZ = abs(int(angles[0]) - int(AZ))
            varEL = abs(int(angles[1]) - int(EL))

            if angles[2]>=14:
                if (varAZ <=1) and (varEL <= 1):

                    print("Posicion Final: ", self.consulta())
                    serial_angulos = self.consulta()

                    activo = False
                    azimut_s = serial_angulos[0]
                    elevacion_s = serial_angulos[1]
                    self.estadoposicion_put(activo, azimut_s, elevacion_s)
                    self.S = False
            else:
                pass

        self.stop()


if __name__ == "__main__":
    global IP
    IP = "192.168.0.108:8000"
    controlador = YaetsuG5500(IP)
    controlador.control(180, 0, 1, 1)
