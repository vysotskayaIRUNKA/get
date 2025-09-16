import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
transistor = 6
state = 0
GPIO.setup(transistor, GPIO.IN)
while True:
    GPIO.output(led, not(GPIO.input(transistor)))
