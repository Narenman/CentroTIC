from machine import ADC
from machine import Pin
import time

def leer_MQ131(pin_adc):
    """ Esta funcion es para leer los
    datos sensor MQ131"""
    Rl = 1000 # Ohms
    Vref = 5  # Volts
    A = 3.12 # de acuerdo a la curva del datasheet
    b = 0.38  # de acuerdo a la curva del datasheet
    Ro = 100 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
    """ Lectura del canal analogico """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    Vo = adc.read()*3.3/1024
    """ Conversion del voltaje a ppm"""
    Rs = Rl*(Vref-Vo)/Vo
    ppm = (A*Ro/Rs)**(1/b)
    return ppm

print("concentracion O3 {} ppm".format(leer_MQ131(34)))