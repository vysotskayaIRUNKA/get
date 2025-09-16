import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
leds = [25, 12, 16]
GPIO.setup(leds, GPIO.OUT)
while True:
    GPIO.output(leds, 0)