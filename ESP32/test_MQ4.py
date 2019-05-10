from machine import ADC
from machine import Pin
import time

def leer_MQ4(pin_adc):
    """ Esta funcion es para leer los
    datos provenientes de los canales del
    ADC"""
    Rl = 1000 # Ohms
    Vref = 5  # Volts
    A = 12.91 # de acuerdo a la curva del datasheet
    b = 0.37  # de acuerdo a la curva del datasheet
    Ro = 1000 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
    """ Lectura del canal analogico """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    Vo = adc.read()*3.3/1024
    """ Conversion del voltaje a ppm"""
    Rs = Rl*(Vref-Vo)/Vo
    ppm = (A*Ro/Rs)**(1/b)
    return ppm

print("concentracion CH4 {} ppm".format(leer_MQ4(35)))