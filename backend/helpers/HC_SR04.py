import time
from RPi import GPIO

class HC_SR04:
    def __init__(self, partrig, parecho) -> None:
        self.trig = partrig
        self.echo = parecho
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def distance(self):
        # Set Trigger to HIGH
        GPIO.output(self.trig, True)
        # Set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        start_time = time.time()
        stop_time = time.time()
        # Save start time
        while GPIO.input(self.echo) == 0:
            start_time = time.time()

        # Save time of arrival
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()

        # Time difference between start and arrival
        time_elapsed = stop_time - start_time
        # Multiply with the sonic speed (34300 cm/s)
        # And divide by 2, because there and back
        distance = (time_elapsed * 34300) / 2

        return distance