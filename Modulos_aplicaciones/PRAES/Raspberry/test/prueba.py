""" Example for using the SGP30 with CircuitPython and the Adafruit library"""
    
import time
import board
import busio
import adafruit_sgp30

import json
import requests

def sgp30():
    """Esta funcion se encarga de realizar las lecturas del sensor
    digital sgp30 para mirar la calidad del aire """
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)       
    # Create library object on our I2C port
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)      
    print("SGP30 serial #", [hex(i) for i in sgp30.serial])       
    sgp30.iaq_init()
    sgp30.set_iaq_baseline(0x8973, 0x8aae)
    eC02 = sgp30.eCO2 #ppm
    tvoc = sgp30.TVOC #ppb
    return eC02, tvoc

def getToken(username, password, IP):
    data = {
    "username": username,
    "password": password}
    URL = "http://"+IP+"/app_praes/token/"
    r = requests.post(URL, data=data)
    print("HTTP status token {}".format(r.status_code))
    token = json.loads(r.content)
    print(token["token"])
    return token

if __name__ == "__main__":
    username = "mario"
    password = "mario"
    IP = "192.168.0.103:8000"
    getToken(username, password, IP)
    eCO2, tvoc = sgp30()
    print("eC02 {} ppm\ttvoc {} ppb".format(eCO2, tvoc))