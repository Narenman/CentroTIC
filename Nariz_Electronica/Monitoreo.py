import threading
import csv
import time
from DataTestSensor import * 

class ThreadSensing():
    def __init__(self,stop_thread=False):
        self.stop_thread = stop_thread
        self.t = object

    
    def escribir_csv(self):
        """ Esta funcion ejecuta un hilo
        para almacenar los datos sensados de la nariz electronica en 
        un archivo .csv
        """
 
        def imprime(num):
            """ Hilo encargado de sensar los datos de la nariz y
            almacenarlos en un archivo .csv"""
            try:
                with open('employee_file'+str(num)+'.csv', mode='w') as employee_file:
                    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    while True:
                        print("hilo care nalga")
                        global stop_thread
                        [fecha, valores] = dsensors()
                        employee_writer.writerow([fecha, valores])
                        if stop_thread:
                            break  
            except:             
                print("joder nariz")

        try:
            self.t = threading.Thread(name="almacenar", target=imprime, args=(0, ))
            self.t.setDaemon(True)
            self.t.start()
        except:
            print("joder hilo")

    def del_hilo(self):
        """ Esta funcion se encarga de parar el sensado de datos cuando el 
        usuario envie la bandera de parada
        """
        stop_thread = True
        self.t.join()
        print("almacenamiento terminado")


if __name__ == "__main__":
    hilo = ThreadSensing(False)
    hilo.escribir_csv()
    time.sleep(3)
    hilo.del_hilo()