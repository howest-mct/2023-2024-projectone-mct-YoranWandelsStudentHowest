import RPi.GPIO as GPIO
import time

class Waterpump:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("Water pump is now ON")

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
        print("Water pump is now OFF")
