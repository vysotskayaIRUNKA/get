import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [24, 22, 23, 27, 17, 25, 12, 16]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
light_time = 0.2
while True:
    for i in leds:
        GPIO.output(i, 1)
        time.sleep(light_time)
        GPIO.output(i, 0)
    for i in leds[::-1]:
        GPIO.output(i, 1)
        time.sleep(light_time)
        GPIO.output(i, 0)