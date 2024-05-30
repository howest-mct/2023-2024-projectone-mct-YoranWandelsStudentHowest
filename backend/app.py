import time
import datetime
from RPi import GPIO
from helpers.HC_SR04 import HC_SR04
from helpers.PCF import PCF
from helpers.LCD import LCD
from helpers.RotaryEncoder import rotaryEncoder
from helpers.StepperMotor import StepperMotor
import threading
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sc3pTr0n3'

socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
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

# button
btn = 18

# HX711
clck = 15
dt = 14

stop_threads = False
RotaryCounter = 0

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

def all_out():
    GPIO.setmode(GPIO.BCM)  # Ensure correct pin numbering mode within the thread
    time_all_out = time.time()
    print('test all_out')
    while not stop_threads:
        if (time.time() - time_all_out) >= 5:
            idwatersensor = (DataRepository.get_id_sensor('Afstand meten om te kijken of er een fles onder de machine staat'))['DeviceID']
            current_datetime = datetime.datetime.now()
            waterdist = round(watersensor.distance(), 2)
            print(f"Water distance: {waterdist} at {current_datetime}")
            create_historiek = DataRepository.create_historiek(idwatersensor, 1, current_datetime, waterdist, 'water afstand sensor test')
            if create_historiek:
                print('New history entry created successfully.')
            time_all_out = time.time()

def start_thread():
    thread = threading.Thread(target=all_out)
    thread.start()
    return thread

def my_callback_one(pin):
    print('button click')

GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btn, GPIO.RISING, bouncetime=200)
GPIO.add_event_callback(btn, my_callback_one)

if __name__ == '__main__':
    try:
        print("**** Starting HC-SR04 Distance Measurement ****")
        # Instantiate HC_SR04 with the appropriate GPIO pins
        watersensor = HC_SR04(trig1, echo1)
        bottlesensor = HC_SR04(trig2, echo2)

        rotary = rotaryEncoder(switch, dt, clk)
        pcf = PCF(sda, scl, adres)
        lcd = LCD(rs, enable, pcf)

        Proteinmotor = StepperMotor([6, 13, 19, 26])
        Creatinemotor = StepperMotor([5, 17, 27, 22])
        # Proteinmotor.draaien_links()

        lcd.clear_display()
        lcd.write_message('hey')
        # thread = start_thread()
        socketio.run(app, debug=False, host='0.0.0.0')
        while True:
            print(rotaryEncoder.counter())
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("Stopping threads and cleaning up GPIO")
        stop_threads = True
        # thread.join()  # Ensure the thread has completed
        GPIO.cleanup()
