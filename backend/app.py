import time
from RPi import GPIO
from helpers.HC_SR04 import HC_SR04
from helpers.PCF import PCF
from helpers.LCD import LCD
from helpers.RotaryEncoder import rotaryEncoder

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LCD
rs = 21
enable = 20

# PCF8574
sda = 2
scl = 3
adres = 0x20

# HC_SR04
trig1 = 9
echo1 = 10
trig2 = 12
echo2 = 11

# Rotary encoder
switch = 23
dt = 24
clk = 25

# Definieer je HC-SR04 klasse


if __name__ == '__main__':
    try:
        print("**** Starting HC-SR04 Distance Measurement ****")
        # Instantiate HC_SR04 with the appropriate GPIO pins
        watersensor = HC_SR04(trig1, echo1)
        bottlesensor = HC_SR04(trig2, echo2)
        rotary = rotaryEncoder(switch, dt, clk)

        pcf = PCF(sda, scl, adres)
        lcd = LCD(rs, enable, pcf)
        
        lcd.clear_display()
        lcd.write_message('hey')
        print('test')
        while True:
            waterdist = watersensor.distance()
            print(f"Measured Distance: {waterdist:.2f} cm")

            bottledist = bottlesensor.distance()
            print(f"Measured Distance: {bottledist:.2f} cm")
            time.sleep(1)  # Sleep for 1 second before next measurement

            command = input("Voer commando in: ")
            if command == "toerlinks":
                draaien_links()
            elif command == "toerrechts":
                draaien_rechts()
            elif command.startswith("X"):
                graden = int(command[1:])
                draaien_rechts_graden(graden)
            elif command.startswith("-X"):
                graden = int(command[2:])
                draaien_links_graden(graden)
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("Cleaning up GPIO")
        GPIO.cleanup()
