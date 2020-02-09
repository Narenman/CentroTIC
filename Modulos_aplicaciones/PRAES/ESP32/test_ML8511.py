from machine import ADC
from machine import Pin
import time

def leer_dato_uv(pin_adc):
    """ Esta funcion es para leer los
    datos provenientes de los canales del ADC
    ademas esta la caracterizacion del sensor UV ML8511
    caracterizacion y = 0.1625x + 1.0
    x = (y - 1.0)/0.1625  mW/cm^2
    """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    y = adc.read()*3.3/1024
    if y < 1:
        x = 0
    else:
        x = (y-1.0)/0.1625
    return x

print(leer_dato_uv(33))

