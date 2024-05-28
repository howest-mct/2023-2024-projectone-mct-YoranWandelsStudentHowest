import time
from RPi import GPIO
from helpers.HC_SR04 import HC_SR04

# Definieer je HC-SR04 klasse


if __name__ == '__main__':
    try:
        print("**** Starting HC-SR04 Distance Measurement ****")
        # Instantiate HC_SR04 with the appropriate GPIO pins
        sensor = HC_SR04(partrig=9, parecho=10)
        
        # Read distance in a loop
        while True:
            dist = sensor.distance()
            print(f"Measured Distance: {dist:.2f} cm")
            time.sleep(1)  # Sleep for 1 second before next measurement
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("Cleaning up GPIO")
        GPIO.cleanup()
