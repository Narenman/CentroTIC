from machine import ADC
from machine import Pin
import time

def leer_MQ(pin_adc, A, b ,Ro):
    """ Esta funcion es para leer los
    datos de los sensores MQ que tienen un comportamiento
    ppm = ARo/Rs**(1/b)"""
    Rl = 1000 # Ohms
    Vref = 5  # Volts
    """ Lectura del canal analogico """
    adc = ADC(Pin(pin_adc))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    Vo = adc.read()*3.3/1024
    if Vo==0:
        Rs = 0.0000000000000000001
        """ Conversion del voltaje a ppm"""
    else:
        Rs = Rl*(Vref-Vo)/Vo
    ppm = (A*Ro/Rs)**(1/b)
    return ppm

#sensor MQ131
# A = 3.12 # de acuerdo a la curva del datasheet
# b = 0.38  # de acuerdo a la curva del datasheet
# Ro = 100 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
# pin_MQ131 = 34
# ppm_mq131 = leer_MQ(pin_MQ131, A, b, Ro)
# print("O3 {} ppm".format(ppm_mq131))

#sensor MQ4
# A = 12.91 # de acuerdo a la curva del datasheet
# b = 0.37  # de acuerdo a la curva del datasheet
# Ro = 1000 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
# pin_MQ4 = 33
# ppm_mq4 = leer_MQ(pin_MQ4,A,b,Ro)
# print("CH4 {} ppm".format(ppm_mq4))

# sensor MQ7
# A = 14.90 # de acuerdo a la curva del datasheet
# b = 0.13  # de acuerdo a la curva del datasheet
# Ro = 100 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
# pin_MQ7 = 39
# ppm_mq7 = leer_MQ(pin_MQ7, A, b, Ro)
# print("lpg {} ppm".format(ppm_mq7))

#sensor MQ9
A = 29.63 # de acuerdo a la curva del datasheet
b = 0.53  # de acuerdo a la curva del datasheet
Ro = 100 # valor usado tentativamente se debe calibrar a 1000 ppm para obtener este valor
pin_MQ9 = 36
ppm_mq9 = leer_MQ(pin_MQ9, A, b, Ro)
print("CO {} ppm".format(ppm_mq9))