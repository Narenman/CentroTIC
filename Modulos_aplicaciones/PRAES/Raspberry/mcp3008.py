import time
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

"""Hardware SPI configuration:
 pines utilizados
 GPIO     MCP3008
 11       CLK
 9        DOUT
 10       DIN
 8        CS  
"""

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Software SPI configuration:
#GPIO       MCP3008
CLK  = 18   #CLK
MISO = 23   #DOUT
MOSI = 24   #DIN
CS   = 25   #CS
mcp1 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

while True:
    values1 = [0]*8
    values = [0]*8

    for i in range(8):
        values[i] = mcp.read_adc(i)*3.3/1023.0
        values1[i] = mcp1.read_adc(i)*3.3/1023.0
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values1))
        print('###################################################################')
        time.sleep(0.5)