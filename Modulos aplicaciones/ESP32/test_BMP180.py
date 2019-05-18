from machine import Pin, I2C
from bmp180 import BMP180

def leer_presion(scl_pin, sda_pin):
    """ Lee la presion del sensor BMP180 """
    bus = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)  # create I2C peripheral at frequency of 400kHz
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

    temp = bmp180.temperature
    p = bmp180.pressure
    altitude = bmp180.altitude
    return p

presion = leer_presion(14,27)
print("presion {} mbar".format(presion))