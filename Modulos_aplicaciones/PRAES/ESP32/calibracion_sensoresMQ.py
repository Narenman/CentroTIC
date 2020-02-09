import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def func_ecn(x,a,b):
    return a*x**(-b)

""" Datos sensor MQ4 para CH4
El  valor de voltaje medido realmente corresponde 
al divisor de tension

Vo = Vref(Rl/(Rl+Rs))      Rl: es la resistencia de carga generalmente 1k
se despeja Rs
Rs = Rl(Vref-Vo)/Vo

Con Rs encontrada ya podemos calcular el ppm
ppm = (ARo/Rs)^(1/b)       A y b son constantes que se sacan de la curva y = Ax^-b

Ro: es la resistencia calculada cuando no hay presencia de gas
"""

ppm = numpy.array([200, 300, 400, 500, 900, 1000,2000, 3000, 4000,6000,7000,10000]) #x
Rs_Ro = numpy.array([1.85,1.55,1.33, 1.2, 1.08, 1, 0.79, 0.61, 0.6,0.5,0.49, 0.45]) #y

popt, pcov = curve_fit(func_ecn, ppm, Rs_Ro)
ecn = r"$y= {0:.2f}$".format(popt[0])+r"$x^{}$".format({-popt[1]})


plt.plot(ppm, func_ecn(ppm, *popt), 'g--', label=ecn)
plt.plot(ppm,Rs_Ro,'o',label="datos curva CH4")
plt.xlabel("ppm")
plt.ylabel("Rs/Ro")
plt.title("Curva del sensor MQ4 para CH4")
plt.legend()
plt.grid(True)
plt.show()
