import RPi.GPIO as GPIO
import time

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
up_arr = 9
down_arr = 10
GPIO.setup(up_arr, GPIO.IN)
GPIO.setup(down_arr, GPIO.IN)
num = 0
sleep_time = 0.2
while True:
    start_time = time.time()
    if (time.time()-start_time <= 1) and GPIO.input(up_arr) and not(GPIO.input(down_arr)):
        num += 1
        if num>255: num=0
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    elif (time.time()-start_time <= 1) and GPIO.input(down_arr) and not(GPIO.input(up_arr)):
        num-=1
        if num<0: num=255
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    elif (time.time()-start_time <= 1) and GPIO.input(down_arr) and GPIO.input(up_arr):
        num=255
        print(num, dec2bin(num))
    for i in range(8):
        if dec2bin(num)[i]: GPIO.output(leds[i], 1)
    GPIO.output(leds, 0)
    time.sleep(1)
