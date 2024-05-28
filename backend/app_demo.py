import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
# gpio
from RPi import GPIO
from helpers.klasseknop import Button

ledPin = 26
btnObject = Button(19)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    btnObject.on_press(lees_knop)

def lees_knop(pin):
    # print('lees knop')
    if btnObject.pressed:
        print("**** button pressed ****")
        if GPIO.input(ledPin) == 1:
            switch_light({ "lamp_id": '3', "new_status": 0 })
        else:
            switch_light({ "lamp_id": '3', "new_status": 1 })



app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def all_out():
    # wait 10s with sleep sintead of threading.Timer, so we can use daemon
    time_all_out = time.time()
    # Record the start time after the initial delay
    # if time.time() - time_all_out >= 10:
    while True:
        if (time.time() - time_all_out) >= 30:
            print('*** We zetten alles uit **')
            DataRepository.update_status_alle_lampen(0)
            status = DataRepository.read_status_lampen()
            socketio.emit('B2F_alles_uit', {
                        'status': "lampen uit"})
            socketio.emit('B2F_status_lampen', {'lampen': status})
            switch_light({ "lamp_id": '3', "new_status": 0 })
            time_all_out = time.time()


def start_thread():
    threading.Timer(10, all_out).start()
    # t = threading.Thread(target=all_out, daemon=True)
    # t.start()
    # print("thread started")


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    status = DataRepository.read_status_lampen()
    # socketio.emit('B2F_status_lampen', {'lampen': status})
    # Beter is het om enkel naar de client te sturen die de verbinding heeft gemaakt.
    emit('B2F_status_lampen', {'lampen': status}, broadcast=False)


@socketio.on('F2B_switch_light')
def switch_light(data):
    print('licht gaat aan/uit', data)
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    # spreek de hardware aan
    # stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)
    print(res)
    # vraag de (nieuwe) status op van de lamp
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    # socketio.emit('B2F_verandering_lamp', {'lamp': data}, broadcast=True)
    # socketio.emit('B2F_verandering_lamp', {'lamp': data})
    # of doe een broadcast
    socketio.emit('B2F_verandering_lamp',  {'lamp': data})
    # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
    if lamp_id == '3':
        print('tv kamer switch')
        if new_status == 1:
            GPIO.output(ledPin, GPIO.HIGH)
        else:
            GPIO.output(ledPin, GPIO.LOW)


if __name__ == '__main__':
    try:
        start_thread()
        setup_gpio()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("done")
        GPIO.cleanup()
