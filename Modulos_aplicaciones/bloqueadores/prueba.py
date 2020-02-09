from Jamming import Jamming
import time

global jamming
def bloqueo(frec_central):
    """Entradas:
    * frec_central para indicar la frecuencia del VCO 78e6 <frec_central <5.92e9 """
    #objeto para realizar el sensado
    jamming = Jamming()
    jamming.start()
    jamming.set_freq(frec_central)
