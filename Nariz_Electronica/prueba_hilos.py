import threading
import csv
import time
# from DataTestSensor import * 

class ThreadSensing():
    def __init__(self,stop_thread=False):
        self.stop_thread = stop_thread
    
    def escribir_csv(self):
        """ Esta funcion ejecuta un hilo
        para almacenar los datos sensados de la nariz electronica en 
        un archivo .csv
        """
        def imprime(num):
            """ Hilo encargado de sensar los datos de la nariz y
            almacenarlos en un archivo .csv"""
            with open('employee_file'+str(num)+'.csv', mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                while True:
                    # [fecha, valores] = dsensors()
                    employee_writer.writerow(["fecha", "valores"])      
                    if self.stop_thread:
                        break

        self.t = threading.Thread(name="almacenar", target=imprime, args=(0, ))
        self.t.setDaemon(True)
        self.t.start()
        
    def terminar_almacenamiento(self):
        """ Esta funcion se encarga de parar el sensado de datos cuando el 
        usuario envie la bandera de parada
        """
        self.stop_thread = True
        self.t.join()
        return self.t.isAlive()

if __name__ == "__main__":
    hilo = ThreadSensing(False)
    hilo.escribir_csv()
    time.sleep(2)
    hilo.terminar_almacenamiento()


