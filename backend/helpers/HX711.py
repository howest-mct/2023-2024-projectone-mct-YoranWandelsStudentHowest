import RPi.GPIO as GPIO
import time
from hx711 import HX711

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin configuration
DOUT_PIN = 14  # Change to your data pin
PD_SCK_PIN = 15  # Change to your clock pin
#2
# DOUT_PIN = 8  # Change to your data pin
# PD_SCK_PIN = 7  # Change to your clock pin

# Create an instance of the HX711 class
hx = HX711(dout_pin=DOUT_PIN, pd_sck_pin=PD_SCK_PIN)

hx.zero()

while True:
    reading = hx.get_data_mean()
    print(reading)