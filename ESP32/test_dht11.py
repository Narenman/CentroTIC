import dht
import machine
d = dht.DHT11(machine.Pin(32))
print(d)
print(d.temperature())
print(d.humidity())