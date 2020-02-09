import serial
import time



#VP2C : VANTAGE PRO 2 CONSOLE SERIAL OBJECT

PORT     = '/dev/ttyS0'
BAUDRATE = 19200
BYTESIZE = serial . EIGHTBITS
PARITY   = serial . PARITY_NONE
STOPBITS = serial . STOPBITS_ONE
XONOFF   = False
TIMEOUT  = 3


w = serial.Serial(PORT, 
                    BAUDRATE, 
                    BYTESIZE, 
                    PARITY, 
                    STOPBITS, 
                    TIMEOUT, 
                    XONOFF)

# perform the console wakeup calls here , ref . Davis documentation

def read():
        w.write('LOOP 1\n'.encode())
    
        data_packet  = list(w.read(100))
        

        if len(data_packet)==100:
                BarTrend     = data_packet[1:][3]
                Barometer    = data_packet[1:][8]  << 8 or data_packet[1:][7]
                InsideTemp   = data_packet[1:][10] << 8 or data_packet[1:][9]
                InsideHumi   = data_packet[1:][11]
                OutSideTemp  = data_packet[1:][13] << 8 or data_packet[1:][12]
                WindSpeed    = data_packet[1:][14]
                AvgWSpeed    = data_packet[1:][15]
                WindDirect   = data_packet[1:][17] << 8 or data_packet[1:][16]
                OutSideHumi  = data_packet[1:][33]
                RainRate     = data_packet[1:][42] << 8 or data_packet[1:][41]
                UV           = data_packet[1:][43]
                SolarRadia   = data_packet[1:][45] << 8 or data_packet[1:][44]
                StormRain    = data_packet[1:][47] << 8 or data_packet[1:][46]


                out = {'Barometric Pressure': Barometer,
                        'Outside Temperature': OutSideTemp,
                        'Inside Temperature': InsideTemp,
                        'Outside Humidity': OutSideHumi,
                        'Wind Direction': WindDirect,
                        'Wind speed': WindSpeed,
                        'Wind AVG': AvgWSpeed,
                        'UV': UV,
                        'Solar Radiation': SolarRadia}
        else:
                out = 0
        

        return out

        
print(read())

# try:
#     table = []
#     c = 0
#     while True:

#         w.write('LOOP 1\n'.encode())
    
#         data_packet  = list(w.read(100))
        

#         if len(data_packet)==100:
#             BarTrend     = data_packet[1:][3]
#             Barometer    = data_packet[1:][8] << 8 or data_packet[1:][7]
#             InsideTemp   = data_packet[1:][10] << 8 or data_packet[1:][9]
#             InsideHumi   = data_packet[1:][11]
#             OutSideTemp  = data_packet[1:][13] << 8 or data_packet[1:][12]
#             WindSpeed    = data_packet[1:][14]
#             AvgWSpeed    = data_packet[1:][15]
#             WindDirect   = data_packet[1:][17] << 8 or data_packet[1:][16]
#             OutSideHumi  = data_packet[1:][33]
#             RainRate     = data_packet[1:][42] << 8 or data_packet[1:][41]
#             UV           = data_packet[1:][43]
#             SolarRadia   = data_packet[1:][45] << 8 or data_packet[1:][44]
#             StormRain    = data_packet[1:][47] << 8 or data_packet[1:][46]
            
#             # table = tabulate([['Barometric Pressure', Barometer],
#             #                 ['Outside Temperature', OutSideTemp],
#             #                 ['Inside Temperature', InsideTemp],
#             #                 ['Outside Humidity', OutSideHumi],
#             #                 ['Inside Humidity', InsideHumi],
#             #                 ['Wind Direction', WindDirect],
#             #                 ['Wind speed', WindSpeed],
#             #                 ['UV', UV],
#             #                 ['Solar Radiation', SolarRadia]], headers=['Variable', 'Readed value'])

#             dicc = {'Barometric Pressure': Barometer,
#                    'Outside Temperature': OutSideTemp,
#                    'Outside Humidity': OutSideHumi,
#                    'Wind Direction': WindDirect,
#                    'Wind speed': WindSpeed,
#                    'UV': UV,
#                    'Solar Radiation': SolarRadia}

#             c += 1
#             print('\r', "| Lectura: ", c,
#                         "| Temperatura: ", InsideTemp, #round((OutSideTemp/10.0-32)*(5.0/9), 2),
#                         "| Humedad: ", OutSideHumi,
#                         "| Presión: ", Barometer,
#                         "| Dir Viento: ", WindDirect,
#                         "| Vel Viento: ", WindSpeed,
#                         "| UV: ", UV,
#                         "| Rad. Solar: ", SolarRadia, sep='', end='', flush=True)

#         else:
#             print('\n No data received', ' Lectura :', c, '\n')   
            

#         time.sleep(3)
        

# except KeyboardInterrupt:
#     print("\r...stopped")
#     pass