import time
from RPi import GPIO

class LCD:
    def __init__(self, rs, enable, pcf):
        self.rs = rs
        self.enable = enable
        self.pcf = pcf
        # Initialiseer alle GPGPIO pinnen.
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)

        time.sleep(0.1)
        self.init_LCD()

    # stuur instructie
    def send_instructGPIOn(self, value):
        # rs laag: voor instructGPIOn
        GPIO.output(self.rs, GPIO.LOW)
        # enable hoog
        GPIO.output(self.enable, GPIO.HIGH)
        self.set_data_bits(value)
        # enable terug laag
        GPIO.output(self.enable, GPIO.LOW)
        time.sleep(0.01)

    # stuur 1 character
    def send_character(self, character):
        # rs hoog: voor data
        GPIO.output(self.rs, GPIO.HIGH)
        # enable hoog
        GPIO.output(self.enable, GPIO.HIGH)
        # data klaarzetten
        self.set_data_bits(character)
        # enable laag
        GPIO.output(self.enable, GPIO.LOW)
        # wait
        time.sleep(0.01)

    # set_data_bits(value)
    def set_data_bits(self, byte):
        self.pcf.write_outputs(byte)

    # write_message(message).
    def write_message(self, message):
        for char in message[:16]:
            self.send_character(ord(char))
        for char in message[16:]:
            self.move_screen()
            self.send_character(ord(char))

    def clear_display(self):
        self.send_instructGPIOn(0b00000001)
        # self.send_instructGPIOn(0b00000010)

    # init_LCD()
    def init_LCD(self):
        # set datalengte op 8 bit (= DB4 hoog), 2 lijnen (=DB3), 5x7 display (=DB2).
        self.send_instructGPIOn(0b00111000)
        # display on (=DB2), cursor on (=DB1), blinking on (=DB0)
        self.send_instructGPIOn(0b00001111)
        # clear display en cursor home (DB0 hoog)
        self.clear_display()

    # set cursor
    def set_cursor(self, row, col):
        # byte maken: row (0 of 1) = 0x0* voor rij 0 of 0x4* voor rij 1. col = 0x*0 - 0x*F
        byte = row << 6 | col
        # byte | 128 want DB7 moet 1 zijn
        self.send_instructGPIOn(byte | 128)

    # move screen: verplaatst het scherm
    def move_screen(self):
        self.send_instructGPIOn(0b00011000)

