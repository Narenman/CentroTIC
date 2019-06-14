from machine import ADC
from machine import Pin
import time

def leer_dato(pin_adc):
    """ Esta funcion es para leer los
    datos provenientes de los canales del
    ADC"""
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    adc_pot = adc.read()*3.0/1024
    return adc_pot

while True:
    print(leer_dato(32))
    time.sleep(300e-3)

