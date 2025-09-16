import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
led = 16
GPIO.setup(led, GPIO.OUT)
while True:
    GPIO.output(led, 0)