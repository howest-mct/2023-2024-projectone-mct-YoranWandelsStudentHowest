import time
from RPi import GPIO

class PCF:
    def __init__(self, SDA, SCL, address):
        self.sda = SDA
        self.scl = SCL
        self.__address = address
        self.delay = 0.002

        # GPIO setup
        self.__setup()

    def write_outputs(self, data: int):
        # data schrijven
        self.__writebyte(data)
        # ack simuleren door 1 bit te writen
        self.__writebit(1)

    @property
    def address(self):
        return self.__address

    # om het adres van het device te wijzigen
    @address.setter
    def address(self, value):
        self.__address = value

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sda, GPIO.OUT)
        GPIO.setup(self.scl, GPIO.OUT)

        time.sleep(0.1)

        # startconditie
        self.__start_conditie()
        # adres doorklokken + RW=0 om te schrijven
        self.__writebyte(self.__address << 1)
        # ack
        self.__ack()

    def __start_conditie(self):
        GPIO.output(self.sda, GPIO.HIGH)
        time.sleep(self.delay)
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)
        GPIO.output(self.sda, GPIO.LOW)
        time.sleep(self.delay)
        GPIO.output(self.scl, GPIO.LOW)
        time.sleep(self.delay)

    def stop_conditie(self):
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)
        GPIO.output(self.sda, GPIO.HIGH)
        time.sleep(self.delay)

    def __writebit(self, bit):
        # sda bitwaarde geven
        GPIO.output(self.sda, bit)
        time.sleep(self.delay)
        # clock hoog
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)
        # clock laag na delay
        GPIO.output(self.scl, GPIO.LOW)
        time.sleep(self.delay)

    def __ack(self):
        # setup input + pullup van sda pin
        GPIO.setup(self.sda, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # klok omhoog brengen
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)
        # sda pin inlezen: laag = OK
        status = GPIO.input(self.sda) == GPIO.LOW
        # setup output van sda pin
        GPIO.setup(self.sda, GPIO.OUT)
        # klok omlaag
        GPIO.output(self.scl, GPIO.LOW)
        time.sleep(self.delay)
        return status

    def __writebyte(self, byte):
        # 8 keer een bit schrijven
        mask = 0x80
        for i in range(8):
            self.__writebit(byte & (mask >> i))