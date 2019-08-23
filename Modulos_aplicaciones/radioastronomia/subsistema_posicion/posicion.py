import requests
import json
""" este archivo contiene lo relacionado al RS232 y 
adquisicion de datos por el rotor
"""
class YaetsuG5500():
    def __init__(self):
        pass
    
    def control(self, azimut, elevacion, region, antena):
        """se encarga de enviarle las instrucciones al YAETSU 5500 """
        print("enviando control\nazimut: {}\televacion: {}".format(azimut, elevacion))

if __name__ == "__main__":

    controlador = YaetsuG5500()