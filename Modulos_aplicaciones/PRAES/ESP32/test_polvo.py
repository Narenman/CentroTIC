from machine import ADC
from machine import Pin
import utime 

def leer_polvo(DPIN, APIN):
    """Definici0n de pines
    para el sensor de polvo GP2Y1010AU0F
    """
    p13 = Pin(DPIN, Pin.OUT)
    adc = ADC(Pin(APIN))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    #proceso de lectura para el sensor
    p13.off()
    utime.sleep_us(280)
    V1 = adc.read()*3.3/1024
    utime.sleep_us(40)
    p13.on()
    utime.sleep_us(9680)  
    dust_density = 0.17*V1-0.1
    return dust_density

dust_density=leer_polvo(13,34)
print("dust_density {} mg/m^3 ". format(dust_density))

