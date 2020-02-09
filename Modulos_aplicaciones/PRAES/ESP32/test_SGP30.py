import adafruit_sgp30
from machine import I2C, Pin

def leer_sgp30(scl_pin, sda_pin):
    """ esta funcion es para leer los datos del sensor
    sgp30 y retorna+
    CO2 en ppm
    TVOC en ppb"""
    i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    co2eq, tvoc = sgp30.iaq_measure()
    return co2eq, tvoc

co2eq, tvoc = leer_sgp30(26,25)
print("CO2 {} ppm\ntvoc {} ppm".format(co2eq, tvoc))