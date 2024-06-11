#!/usr/bin/env python3
import pickle
import os

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
# HX711
hx1_clck = 15
hx1_dt = 14

hx2_clck = 16
hx2_dt = 1

try:
    GPIO.setmode(GPIO.BCM) 
    hx_protein = HX711(dout_pin=hx1_dt, pd_sck_pin=hx1_clck)
    hx_creatine = HX711(dout_pin=hx2_dt, pd_sck_pin=hx2_clck)

    # Check if we have swap file. If yes that suggest that the program was not
    # terminated proprly (power failure). We load the latest state.
    swap_file_creatine = 'creatine.swp'
    if os.path.isfile(swap_file_creatine):
        with open(swap_file_creatine, 'rb') as swap_file:
            hx_creatine = pickle.load(swap_file)

    swap_file_protein = 'protein.swp'
    if os.path.isfile(swap_file_protein):
        with open(swap_file_protein, 'rb') as swap_file:
            hx_protein = pickle.load(swap_file)
    
    while True:
        try:
            print('proteine',hx_protein.get_weight_mean(20), 'g')
            print('creatine', hx_creatine.get_weight_mean(20), 'g')
        except:
            print('error')

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()