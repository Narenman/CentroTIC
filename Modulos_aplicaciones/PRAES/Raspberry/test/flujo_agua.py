import RPi.GPIO as GPIO
import time, sys


def flujo_agua():
    GPIO.setmode(GPIO.BOARD)
    inpt = 33
    GPIO.setup(inpt,GPIO.IN)
    constante = 0.10

    time_new = time.time() + 1
    rate_cnt = 0
    while time.time() <= time_new:
        try:
            if GPIO.input(inpt)!=0:
                rate_cnt +=1
        except:
            print('\nCTRL C - Exiting nicely')
            GPIO.cleanup()
            sys.exit()

    print('\nLiters / min ', round(rate_cnt*constante,4))
    print('Time (min & clock) ', '\t', time.asctime(time.localtime(time.time())),'\n')
    print('Done')
    return rate_cnt*constante

if __name__ == "__main__":
    while True:
        time.sleep(1)
        print(flujo_agua())
