import serial
import time
import sys

PORT 		= '/dev/ttyUSB0'
BAUDRATE 	= 9600
BYTESIZE 	= serial.EIGHTBITS
PARITY		= serial.PARITY_NONE
STOPBITS	= serial.STOPBITS_ONE

gs232b = serial.Serial(PORT, BAUDRATE, BYTESIZE, PARITY, STOPBITS)

gs232b.flush()

gs232b.write(b'\r')
TC = 'W{} {}\r'.format(sys.argv[1], sys.argv[2])
gs232b.write(TC.encode())
LINE = gs232b.read()
print("LINEA", LINE)
s = True

#while S:
#    gs232b.write(b'C2\r')
#    line = gs232b.readline()
#    print("   -", line)
#    time.sleep(1)
time.sleep(15)

gs232b.flushInput()

gs232b.write(b'C2\r')
l = gs232b.read(14)
print(l)

gs232b.flushInput()


gs232b.write(b'C2\r')
l = gs232b.read(14)
print(l)

gs232b.flushInput()


gs232b.write(b'C2\r')
l = gs232b.read(14)
ll = str(l)[1:]
print(l, len(l), type(l), ll, type(ll))




gs232b.close()
print("Serial Closed")

