import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
leds = [22, 23, 27, 17]
GPIO.setup(leds, GPIO.OUT)
while True:
    GPIO.output(leds, 0)