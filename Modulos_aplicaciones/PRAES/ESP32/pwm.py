from machine import Pin
# from machine import PWM
import time

p26 = Pin(26, Pin.OUT)
while True:
    #pwm2 = PWM(Pin(26), freq=600, duty=500) # create and configure in one go
    p26.on()
    time.sleep(120)
    #pwm2 = PWM(Pin(26), freq=600, duty=0)
    p26.off()
    time.sleep(30*60)