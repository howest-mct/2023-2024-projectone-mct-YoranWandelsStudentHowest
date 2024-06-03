import time
import datetime
from RPi import GPIO
from helpers.HC_SR04 import HC_SR04
from helpers.PCF import PCF
from helpers.LCD import LCD
from helpers.RotaryEncoder import rotaryEncoder
from helpers.StepperMotor import StepperMotor
from helpers.HX711 import HX711
from helpers.Waterpump import Waterpump
import threading
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

endpoint = '/api/v1'

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
rot_switch = 23
rot_dt = 24
rot_clk = 25

# button
btn = 18

# HX711
hx1_clck = 15
hx1_dt = 14

hx2_clck = 16
hx2_dt = 1

# waterpump
wp_pin = 0


stop_threads = False
RotaryCounter = 0

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/historiek/', methods=['GET'])
def get_bestemmingen():
    if request.method == 'GET':
        historiek = DataRepository.read_historiek()
        if historiek is not None:
            return jsonify(historiek=historiek), 200
        else:
            return jsonify(message='error'), 404

@app.route(endpoint + '/waterlevel/', methods=["GET"])
def get_waterlevel():
    if request.method == 'GET':
        waterlevel = DataRepository.get_latest_waterlevel()
        if waterlevel is not None:
            return jsonify(waterlevel=waterlevel), 200
        else:
            return jsonify(message='error'), 404
        
@app.route(endpoint + '/proteinweight/', methods=["GET"])
def get_proteinweight():
    if request.method == 'GET':
        proteinweight = DataRepository.get_latest_proteinweight()
        if proteinweight is not None:
            return jsonify(proteinweight=proteinweight), 200
        else:
            return jsonify(message='error'), 404
        
@app.route(endpoint + '/creatineweight/', methods=["GET"])
def get_creatineweight():
    if request.method == 'GET':
        creatineweight = DataRepository.get_latest_creatineweight()
        if creatineweight is not None:
            return jsonify(creatineweight=creatineweight), 200
        else:
            return jsonify(message='error'), 404

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

def send_data_watersensor():
    idwatersensor = (DataRepository.get_id_sensor('Afstand meten meten om te kijken hoeveel water er nog in de bidon zit'))['DeviceID']
    current_datetime = datetime.datetime.now()
    waterdist = round(watersensor.distance(), 2)
    print(f"Water distance: {waterdist} at {current_datetime}")
    create_historiek = DataRepository.create_historiek(idwatersensor, 1, current_datetime, waterdist, 'water afstand sensor test')
    if create_historiek:
        print('New history entry created successfully.')
        socketio.emit('B2F_waterlevel', {'waterlevel': waterdist})

def send_data_bottlesensor():
    idbottlesensor = (DataRepository.get_id_sensor('Afstand meten om te kijken of er een fles onder de machine staat'))['DeviceID']
    current_datetime = datetime.datetime.now()
    bottledist = round(bottlesensor.distance(), 2)
    bottlestatus = 1 if bottledist < 100 else 0
    print(f"Bottle acknowledged - distance: {bottledist} at {current_datetime}")
    create_historiek = DataRepository.create_historiek(idbottlesensor, 1, current_datetime, bottledist, 'bottle sensor test')
    if create_historiek:
        print('New history entry created successfully.')
        socketio.emit('B2F_bottlestatus', {'status': bottlestatus})

def send_data_proteinweight():
    try:
        idproteinweight = (DataRepository.get_id_sensor('Gewicht meten van de proteine'))['DeviceID']
        current_datetime = datetime.datetime.now()
        proteinweight = hx_protein.get_weight_mean()
        print(f"Protein Weight: {proteinweight} at {current_datetime}")
        create_historiek = DataRepository.create_historiek(idproteinweight, 1, current_datetime, proteinweight, 'protein weight test')
        if create_historiek:
            print('New history entry created successfully.')
            socketio.emit('B2F_proteinweight', {'weight': proteinweight})
    except:
        print('protein weight error')

def send_data_creatineweight():
    try:
        idcreateineweight = (DataRepository.get_id_sensor('Gewicht meten van de creatine'))['DeviceID']
        current_datetime = datetime.datetime.now()
        creatineweight = hx_creatine.get_data_mean()
        print(f"Creatine Weight: {creatineweight} at {current_datetime}")
        create_historiek = DataRepository.create_historiek(idcreateineweight, 1, current_datetime, creatineweight, 'creatine weight test')
        if create_historiek:
            print('New history entry created successfully.')
            socketio.emit('B2F_creatineweight', {'weight': creatineweight})
    except:
        print('creatine weight error')

def read_sensors():
    GPIO.setmode(GPIO.BCM)  # Ensure correct pin numbering mode within the thread
    time_all_out = time.time()
    print('**** Reading sensors ****')
    while not stop_threads:
        if (time.time() - time_all_out) >= 5:
            send_data_watersensor()
            send_data_bottlesensor()
            send_data_proteinweight()
            send_data_creatineweight()
            time_all_out = time.time()

def start_thread():
    thread = threading.Thread(target=read_sensors)
    thread.start()
    return thread

def my_callback_one(pin):
    print('button click')

GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btn, GPIO.RISING, bouncetime=200)
GPIO.add_event_callback(btn, my_callback_one)

if __name__ == '__main__':
    try:
        watersensor = HC_SR04(trig1, echo1)
        bottlesensor = HC_SR04(trig2, echo2)

        pcf = PCF(sda, scl, adres)
        lcd = LCD(rs, enable, pcf)
        rotary = rotaryEncoder(rot_switch, rot_dt, rot_clk, lcd)

        Proteinmotor = StepperMotor([6, 13, 19, 26])
        Creatinemotor = StepperMotor([5, 17, 27, 22])

        hx_protein = HX711(dout_pin=hx1_dt, pd_sck_pin=hx1_clck)
        hx_creatine = HX711(dout_pin=hx2_dt, pd_sck_pin=hx2_clck)

        waterpump = Waterpump(wp_pin)
        # try:
        #     hx_protein.zero()
        #     hx_creatine.zero()
        #     proteinmean = hx_protein.get_data_mean(readings=100)
        #     creatinemean = hx_creatine.get_data_mean(readings=100)
        #     value = 1
        #     ratio_protein = proteinmean/value
        #     ratio_creatine = creatinemean/value
        #     hx_protein.set_scale_ratio(ratio_protein)
        #     hx_creatine.set_scale_ratio(ratio_creatine)
        # except Exception as ex:
        #     print(ex)
        

        thread = start_thread()
        socketio.run(app, debug=False, host='0.0.0.0')
        # while True:
        #     try:
        #         current_datetime = datetime.datetime.now()
        #         proteinweight = hx_protein.get_raw_data_mean()
        #         print(f"Protein Weight: {proteinweight} at {current_datetime}")
        #         current_datetime = datetime.datetime.now()
        #         creatineweight = hx_creatine.get_raw_data_mean()
        #         print(f"Creatine Weight: {creatineweight} at {current_datetime}")
        #         # time.sleep(1)
        #     except Exception as ex:
        #         print(ex)
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("Stopping threads and cleaning up GPIO")
        stop_threads = True
        thread.join()  # Ensure the thread has completed
        GPIO.cleanup()
