import RPi.GPIO as gpio
import time

class rotaryEncoder:
    def __init__(self, parswitch, pardt, parclk) -> None:
        self.sw = parswitch
        self.dt = pardt
        self.clk = parclk

        self.counter = 0
        self.clkLastState = 0

        gpio.setmode(gpio.BCM)
        gpio.setup(self.dt, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.clk, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.sw, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(self.clk, gpio.BOTH, callback=self.rotation_callback, bouncetime=1)
        gpio.add_event_detect(self.sw, gpio.FALLING, self.switch_callback, bouncetime=200)

    def rotation_callback(self, pin):
        dt_val = gpio.input(self.dt)
        clk_val = gpio.input(self.clk)

        if clk_val!= self.clkLastState and clk_val == False:
            if dt_val != clk_val:
                self.counter += 1
            else:
                self.counter -= 1
            print(self.counter % 3)
        self.clkLastState = clk_val

    # @property
    # def counter(self):
    #     counter = self.counter
    #     return counter

    def switch_callback(self, sw):
        print("rotary switch")