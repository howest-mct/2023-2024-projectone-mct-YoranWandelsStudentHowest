import RPi.GPIO as gpio
from subprocess import check_output
import time

class rotaryEncoder:
    def __init__(self, parswitch, pardt, parclk, parlcd) -> None:
        self.sw = parswitch
        self.dt = pardt
        self.clk = parclk
        self.lcd = parlcd  # Add this line

        self.counter = 0
        self.clkLastState = 0
        self.switchclick = 0
        self.lastswitchclick = 0

        self.clickc1 = False
        self.clickc2 = False
        self.clickc3 = False

        self.powder = 'proteine'
        self.powderamount = 100
        self.wateramount = 100

        self.measurments = 0

        gpio.setmode(gpio.BCM)
        gpio.setup(self.dt, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.clk, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.sw, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(self.clk, gpio.BOTH, callback=self.rotation_callback, bouncetime=1)
        gpio.add_event_detect(self.sw, gpio.FALLING, self.switch_callback, bouncetime=200)

    
    # ********** property counter - (setter/getter) ***********
    @property
    def counter(self) -> int:
        """ The counter property. """
        return self.__counter % 3
    
    @counter.setter
    def counter(self, value: int) -> None:
        self.__counter = value

    # ********** property selectiecounter - (setter/getter) ***********
    @property
    def selectiecounter(self) -> int:
        """ The counter property. """
        return self.__counter % 2
    
    @selectiecounter.setter
    def selectiecounter(self, value: int) -> None:
        self.__counter = value

    
    # ********** property measurements - (setter/getter) ***********
    @property
    def measurements(self) -> int:
        """ The counter property. """
        return (self.__counter % 11) * 50
    
    @measurements.setter
    def measurements(self, value: int) -> None:
        self.__counter = value
    

    def rotation_callback(self, pin):
        dt_val = gpio.input(self.dt)
        clk_val = gpio.input(self.clk)

        if clk_val!= self.clkLastState and clk_val == False:
            if dt_val != clk_val:
                self.__counter += 1
            else:
                self.__counter -= 1
            # print(self.counter)
            self.update_lcd()
            print(self.measurements)
        self.clkLastState = clk_val

    def update_lcd(self):
        if self.clickc1 == True:
            if self.selectiecounter % 2 == 0:
                self.lcd.send_instruction(0b11000000) # Move to second line
                self.lcd.write_message('Proteine') # Write 'Proteine' and clear rest of the line
                self.powder = 'proteine'
            elif self.selectiecounter % 2 == 1:
                self.lcd.send_instruction(0b11000000) # Move to second line
                self.lcd.write_message('Creatine') # Write 'Creatine' and clear rest of the line
                self.powder = 'creatine'
        elif self.clickc2 == True:
            self.lcd.send_instruction(0b11000000) #new line
            self.powderamount = self.measurements
            self.lcd.write_message(f'{self.measurements}')
        elif self.clickc3 == True:
            self.lcd.send_instruction(0b11000000) #new line
            self.wateramount = self.measurements
            self.lcd.write_message(f'{self.measurements}')
        elif self.clickc1 == False & self.clickc2 == False & self.clickc3 == False:
            if self.counter == 0:
                self.lcd.clear_display()
                ips = check_output(['hostname', '--all-ip-addresses']).decode() #decode: bytes -> string
                self.lcd.write_message(ips[:16])
                self.lcd.send_instruction(0b11000000) #new line
                self.lcd.write_message(ips[16:29])
            elif self.counter == 1:
                self.lcd.clear_display()
                self.lcd.write_message('Maak een shake')
                
            else:
                self.lcd.clear_display()
                self.lcd.write_message('3')


    def switch_callback(self, sw):
        if self.switchclick == 0:
            self.switchclick = 1
        else:
            self.switchclick = 0
        if self.switchclick != self.lastswitchclick:
            if self.clickc1 == True:
                print(self.powder)
                self.clickc1 = False
                self.clickc2 = True
                self.lcd.clear_display()
                self.lcd.write_message('aantal gram:')
            elif self.clickc2 == True:
                self.clickc2 = False
                self.clickc3 = True
                self.lcd.clear_display()
                self.lcd.write_message('water (ml):')
            elif self.clickc3 == True:
                print(f'Powder: {self.powder}, Amount: {self.powderamount}g, Water: {self.wateramount}ml')
                self.clickc3 = False
                self.lcd.clear_display()
            elif self.counter == 1:
                self.lcd.clear_display()
                self.lcd.write_message('Selectie poeder:')
                self.lcd.send_instruction(0b11000000) #new line
                self.lcd.write_message('Proteine')
                self.clickc1 = True
            print(self.counter)
        self.lastswitchclick = self.switchclick
        print(self.switchclick)