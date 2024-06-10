import RPi.GPIO as GPIO
import time

class StepperMotor:
    # Pin configuratie
    def __init__(self, pins) -> None:
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

        # Stap sequenties
        self.steps = [
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 1]
        ]
        self.theStep = 0



    # Functie om stap uit te voeren
    def do_step(self, n):
        for i in range(4):
            GPIO.output(self.pins[i], self.steps[n][i])
        time.sleep(0.0009)


    # Draai naar rechts met een bepaald aantal graden
    def draaien_rechts_graden(self, graden):
        stappen = int(graden * (4096 / 360))
        print("Graden_Rechts:", graden)
        print("Stappen_Rechts:", stappen)
        for i in range(stappen):
            self.do_step(self.theStep)
            self.theStep = (self.theStep + 1) % 8

    # Draai naar rechts
    def draaien_rechts(self, theRange):
        for i in range(theRange): # 19505 stappen == 20 seconden, 1 gram poeder
            self.do_step(self.theStep)
            self.theStep = (self.theStep + 1) % 8

    # Draai naar links
    def draaien_links(self,theRange=19505):
        global theStep
        for i in range(theRange): # 19505 stappen == 20 seconden, 1 gram poeder
            self.do_step(self.theStep)
            self.theStep = (self.theStep - 1) % 8

    # Draai naar links met een bepaald aantal graden
    def draaien_links_graden(self, graden):
        stappen = int(graden * (4096 / 360))
        print("Graden_Links:", graden)
        print("Stappen_Links:", stappen)
        for i in range(stappen):
            self.do_step(self.theStep)
            self.theStep = (self.theStep - 1) % 8
