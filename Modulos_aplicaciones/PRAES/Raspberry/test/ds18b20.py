import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

_direccion = '/sys/bus/w1/devices/'
dispositivo_folder = glob.glob(_direccion + '28*')[0]
dispositivo_pad = dispositivo_folder + '/w1_slave'

def leer_temperatura():
    f = open(dispositivo_pad, 'r')
    lineas = f.readlines()
    f.close()
    return lineas

def determinar_valores():
    lineas = leer_temperatura()
    while lineas[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lineas = leer_temperatura()
    igual_pos = lineas[1].find('t=')
    if igual_pos != -1:
        temp_string = lineas[1][igual_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
        
while True:
 print("centigrados,fahrenheit")
 print(determinar_valores()) 
 time.sleep(1)