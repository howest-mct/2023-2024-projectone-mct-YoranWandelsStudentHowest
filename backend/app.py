import time
import datetime
from RPi import GPIO
from helpers.HC_SR04 import HC_SR04
from helpers.PCF import PCF
from helpers.LCD import LCD
# from helpers.RotaryEncoder import rotaryEncoder
from helpers.StepperMotor import StepperMotor
from helpers.Waterpump import Waterpump
import threading
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from hx711 import HX711
import bcrypt # om wachtwoorden te hashen
import pickle # om hx711 calibrate op te vragen
import os # om hx711 calibrate op te vragen
from subprocess import check_output
time.sleep(5)

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

# account
userid = 1
#bottlesensor
bottlestatus = 0
#weight
proteinweight = 0
caseproteinweight = 160
creatineweight = 0
casecreatineweight = 160

#water
waterdist = 0 #max 24

class rotaryEncoder:
    def __init__(self, parswitch, pardt, parclk, parlcd, parwaterpump, parproteinmotor, parcreatinemotor) -> None:
        self.sw = parswitch
        self.dt = pardt
        self.clk = parclk
        self.lcd = parlcd
        self.waterpump = parwaterpump
        self.proteinmotor = parproteinmotor
        self.creatinemotor = parcreatinemotor

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

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.clk, GPIO.BOTH, callback=self.rotation_callback, bouncetime=1)
        GPIO.add_event_detect(self.sw, GPIO.FALLING, self.switch_callback, bouncetime=200)

    
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

    
    # ********** property measurements_powder - (setter/getter) ***********
    @property
    def measurements_powder(self) -> int:
        """ The counter property. """
        return (self.__counter % 11)
    
    @measurements_powder.setter
    def measurements_powder(self, value: int) -> None:
        self.__counter = value

    @property
    def measurements_water(self) -> int:
        """ The counter property. """
        return (self.__counter % 11) * 50
    
    @measurements_water.setter
    def measurements_water(self, value: int) -> None:
        self.__counter = value
    
    def send_data_shake(self):
        global userid
        print(userid)
        if self.powder == 'proteine':
            idpowdermotor = (DataRepository.get_id_sensor('Stappenmotor om de auger te laten draaien van de proteine'))['DeviceID']
        else:
            idpowdermotor = (DataRepository.get_id_sensor('Stappenmotor om de auger te laten draaien van de creatine'))['DeviceID']
        current_datetime = datetime.datetime.now()
        print(f"new shake {self.powder}: {self.powderamount} at {current_datetime}")
        create_historiek = DataRepository.create_historiek(idpowdermotor, userid, current_datetime, self.powderamount, 'nieuwe shake aangemaakt')
        if create_historiek:
            print('New history entry created successfully.')
        print('waterpomp data')
        idwaterpomp = (DataRepository.get_id_sensor('Waterpomp om water te pompen'))['DeviceID']
        create_historiek = DataRepository.create_historiek(idwaterpomp, userid, current_datetime, self.wateramount, 'nieuwe shake aangemaakt')
        if create_historiek:
            print('New history entry created successfully.')
        socketio.emit('B2F_shake', {'shakeamount': self.powderamount})

    def create_shake(self, powder='proteine', powderamount=1, wateramount=100):
            if bottlestatus:
                if (powder == 'proteine' and powderamount <= proteinweight) or (powder == 'creatine' and powderamount <= creatineweight):
                    if wateramount == 0 or waterdist < 23:
                        
                        lcd.clear_display()
                        lcd.write_message('Creating shake')
                        # Bereken de tijd die de waterpomp aan moet staan
                        # 100 ml kost 7 seconden, dus 1 ml kost 7/100 seconden
                        tijd_per_ml = 7 / 100.0
                        benodigde_tijd = wateramount * tijd_per_ml
                        
                        # Bereken het aantal stappen voor de poederdispenser
                        stappen_per_gram = 19505 
                        benodigde_stappen = stappen_per_gram * powderamount
                        
                        # Start de poederdispenser voor het benodigde aantal stappen
                        if self.powder == 'proteine':
                            self.proteinmotor.draaien_links(benodigde_stappen)
                        else:
                            self.creatinemotor.draaien_rechts(benodigde_stappen)

                        # Start de waterpomp
                        self.waterpump.turn_on()
                        # Wacht voor de berekende tijd om water te doseren
                        time.sleep(benodigde_tijd)
                        # Stop de waterpomp
                        self.waterpump.turn_off()
                        lcd.clear_display()
                        lcd.write_message('Shake klaar')
                        self.send_data_shake()
                    else:
                        lcd.clear_display()
                        lcd.write_message('Not enough water left')
                else:
                    lcd.clear_display()
                    lcd.write_message('Not enough powder left')
            else:
                lcd.clear_display()
                lcd.write_message('No bottle present')

    def rotation_callback(self, pin):
        dt_val = GPIO.input(self.dt)
        clk_val = GPIO.input(self.clk)

        if clk_val!= self.clkLastState and clk_val == False:
            if dt_val != clk_val:
                self.__counter += 1
            else:
                self.__counter -= 1
            # print(self.counter)
            self.update_lcd()
            # print(self.measurements_powder)
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
            powder_display = f'{self.measurements_powder:02}' if self.measurements_powder < 10 else str(self.measurements_powder)
            self.powderamount = self.measurements_powder
            self.lcd.write_message(powder_display)
        elif self.clickc3 == True:
            self.lcd.send_instruction(0b11000000) #new line
            water_display = f'{self.measurements_water:03}' if self.measurements_water < 100 else str(self.measurements_water)
            self.wateramount = self.measurements_water
            self.lcd.write_message(water_display)
        elif self.clickc1 == False and self.clickc2 == False and self.clickc3 == False:
            if self.counter == 0:
                self.lcd.clear_display()
                ips = check_output(['hostname', '--all-ip-addresses']).decode() #decode: bytes -> string
                ip_list = ips.split()
                if ip_list:
                    ip_address = ip_list[0]  # Neem het eerste IP-adres
                else:
                    ip_address = "No IP address"  # Fallback als er geen IP-adres is
                
                self.lcd.clear_display()
                self.lcd.write_message(ip_address)  # Schrijf het IP-adres naar het LCD
            elif self.counter == 1:
                self.lcd.clear_display()
                self.lcd.write_message('Maak een shake')
            else:
                self.lcd.clear_display()
                self.lcd.write_message(f'Protein: {proteinweight} g')
                self.lcd.send_instruction(0b11000000) # new line
                self.lcd.write_message(f'Creatine: {creatineweight} g')
                time.sleep(3)  # Display for 3 seconds

                # Display water
                max_distance = 24.0  # afstand als de container leeg is
                min_distance = 10.0   # afstand als de container vol is
                global waterdist

                # Bereken het waterniveau als een percentage
                water_level_percentage = ((max_distance - waterdist) / (max_distance - min_distance)) * 100

                # Bepaal de waterniveau beschrijving
                if water_level_percentage > 66:
                    water_level_description = "Hoog"
                elif water_level_percentage > 33:
                    water_level_description = "Gemiddeld"
                else:
                    water_level_description = "Laag"

                # Weergave van het waterniveau
                self.lcd.clear_display()
                self.lcd.write_message(f'Water level:')
                self.lcd.send_instruction(0b11000000) # new line
                self.lcd.write_message(water_level_description)



    def switch_callback(self, sw):
        if self.switchclick == 0:
            self.switchclick = 1
        else:
            self.switchclick = 0
        if self.switchclick != self.lastswitchclick:
            if self.clickc1 == True:
                # print(self.powder)
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
                global stop_threads
                print(f'Powder: {self.powder}, Amount: {self.powderamount}g, Water: {self.wateramount}ml')
                # stop_threads = True
                self.create_shake(self.powder, self.powderamount, self.wateramount)
                # stop_threads = False
                # Restart the thread
                start_thread()
                self.clickc3 = False
            elif self.counter == 1:
                self.lcd.clear_display()
                self.lcd.write_message('Selectie poeder:')
                self.lcd.send_instruction(0b11000000) #new line
                self.lcd.write_message('Proteine')
                self.clickc1 = True
            # print(self.counter)
        self.lastswitchclick = self.switchclick
        # print(self.switchclick)

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
        
@app.route(endpoint + '/shakehist/', methods=['GET'])
def get_shake_data_user():
    if request.method == 'GET':
        shakehistory = DataRepository.get_user_shake_data(userid)
        if shakehistory is not None:
            return jsonify(shake_history=shakehistory), 200
        else:
            return jsonify(message='error'), 404


@app.route(endpoint + '/gebruiker/', methods=["POST"])
def create_gebruiker():
    if request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        current_datetime = datetime.datetime.now()
        hashed_password = bcrypt.hashpw(gegevens['Wachtwoord'].encode('utf-8'), bcrypt.gensalt())
        new_gebruiker = DataRepository.create_gebruiker(gegevens['Gebruikersnaam'], hashed_password.decode('utf-8'), gegevens['Email'], current_datetime)
        return jsonify(gebruikerid=new_gebruiker), 201


@app.route(endpoint + '/inloggen/', methods=["POST"])
def login_gebruiker():
    if request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        user = DataRepository.get_user_by_email(gegevens['Email'])
        
        if user and bcrypt.checkpw(gegevens['Wachtwoord'].encode('utf-8'), user['Wachtwoord'].encode('utf-8')):
            global userid
            userid = user['GebruikerID']
            print(userid)
            return jsonify(gebruikerid=userid), 200
        else:
            print('foute gegevens')
            return jsonify(error='Incorrect email or password. Please try again.'), 200
        
@app.route(endpoint + '/uitloggen/', methods=["POST"])
def logout_gebruiker():
    if request.method == 'POST':
        global userid
        userid = 1
        return jsonify(logout='succes'), 200

@app.route(endpoint + '/createshake/', methods=["POST"])
def create_shake_front():
    if request.method == 'POST':
        global userid, stop_threads, proteinweight, creatineweight
        gegevens = DataRepository.json_or_formdata(request)
        powder = str(gegevens['Powder'])
        powderAmount = int(gegevens['PowderAmount'])
        waterAmount = int(gegevens['WaterAmount'])
        # Bereken de tijd die de waterpomp aan moet staan
        # 100 ml kost 7 seconden, dus 1 ml kost 7/100 seconden
        if bottlestatus:
            if (powder == 'Protein' and powderAmount <= proteinweight) or (powder == 'Creatine' and powderAmount <= creatineweight):
                if waterAmount == 0 or waterdist < 23:

                    stop_threads = True

                    tijd_per_ml = 7 / 100.0
                    benodigde_tijd = waterAmount * tijd_per_ml
                    
                    # Bereken het aantal stappen voor de poederdispenser
                    stappen_per_gram = 19505 
                    benodigde_stappen = stappen_per_gram * powderAmount
                    # Start de poederdispenser voor het benodigde aantal stappen
                    if powder == 'Protein':
                        Proteinmotor.draaien_links(benodigde_stappen)
                    else:
                        Creatinemotor.draaien_rechts(benodigde_stappen)
                    # Start de waterpomp
                    waterpump.turn_on()
                    # Wacht voor de berekende tijd om water te doseren
                    time.sleep(benodigde_tijd)
                    # Stop de waterpomp
                    waterpump.turn_off()
                    print('shake klaar')
                    stop_threads = False
                    # Restart the thread
                    start_thread()
                    if powder == 'Protein':
                        idpowdermotor = (DataRepository.get_id_sensor('Stappenmotor om de auger te laten draaien van de proteine'))['DeviceID']
                    else:
                        idpowdermotor = (DataRepository.get_id_sensor('Stappenmotor om de auger te laten draaien van de creatine'))['DeviceID']
                    current_datetime = datetime.datetime.now()
                    print(f"new shake {powder}: {powderAmount} at {current_datetime}")
                    create_historiek = DataRepository.create_historiek(idpowdermotor, userid, current_datetime, powderAmount, 'nieuwe shake aangemaakt')
                    if create_historiek:
                        print('New history entry created successfully.')
                    #waterpump
                    idwaterpomp = (DataRepository.get_id_sensor('Waterpomp om water te pompen'))['DeviceID']
                    create_historiek = DataRepository.create_historiek(idwaterpomp, userid, current_datetime, waterAmount, 'nieuwe shake aangemaakt')
                    if create_historiek:
                        print('New history entry created successfully.')
                    socketio.emit('B2F_shake', {'shakeamount': powderAmount, 'deviceid': idpowdermotor})
                    return jsonify(status='succes'), 200
                else:
                    return jsonify(status='Not enough water left'), 200
            else:
                return jsonify(status='Not enough powder left'), 200
        else:
            return jsonify(status='No bottle present'), 200

@app.route(endpoint + '/shutdown/', methods=["POST"])
def shutdown():
    if request.method == 'POST':
        os.system("sudo shutdown -h now")
        return jsonify(status='shutdown'), 200



# SOCKET IO


@socketio.on('connect')
def initial_connection():
    print('A new client connected')


def send_data_watersensor():
    global userid, waterdist
    print(userid)
    idwatersensor = (DataRepository.get_id_sensor('Afstand meten meten om te kijken hoeveel water er nog in de bidon zit'))['DeviceID']
    current_datetime = datetime.datetime.now()
    waterdist = round(watersensor.distance(), 2)
    print(f"Water distance: {waterdist} at {current_datetime}")
    create_historiek = DataRepository.create_historiek(idwatersensor, userid, current_datetime, waterdist, 'water afstand sensor')
    if create_historiek:
        print('New history entry created successfully.')
    socketio.emit('B2F_waterlevel', {'waterlevel': waterdist})


def send_data_bottlesensor():
    global userid, bottlestatus
    idbottlesensor = (DataRepository.get_id_sensor('Afstand meten om te kijken of er een fles onder de machine staat'))['DeviceID']
    current_datetime = datetime.datetime.now()
    bottledist = round(bottlesensor.distance(), 2)
    bottlestatus = 1 if bottledist < 20 else 0
    print(f"Bottle acknowledged - distance: {bottledist} at {current_datetime}")
    create_historiek = DataRepository.create_historiek(idbottlesensor, userid, current_datetime, bottledist, 'bottle sensor ')
    if create_historiek:
        print('New history entry created successfully.')
    socketio.emit('B2F_bottlestatus', {'status': bottlestatus})


def send_data_proteinweight():
    global userid, proteinweight
    try:
        idproteinweight = (DataRepository.get_id_sensor(
            'Gewicht meten van de proteine'))['DeviceID']
        current_datetime = datetime.datetime.now()
        calculated_weight = round(hx_protein.get_weight_mean(20) - caseproteinweight, 2)
        
        # Check if the calculated weight is below -100
        if calculated_weight >= -100:
            proteinweight = calculated_weight
            print(f"Protein Weight: {proteinweight} at {current_datetime}")
            create_historiek = DataRepository.create_historiek(idproteinweight, userid, current_datetime, proteinweight, 'protein weight')
            if create_historiek:
                print('New history entry created successfully.')
            socketio.emit('B2F_proteinweight', {'weight': proteinweight})
        else:
            print(f"Invalid protein weight value: {calculated_weight}, not updating proteinweight.")
    except Exception as e:
        print(f'Protein weight error: {e}')



def send_data_creatineweight():
    global userid, creatineweight
    try:
        idcreateineweight = (DataRepository.get_id_sensor(
            'Gewicht meten van de creatine'))['DeviceID']
        current_datetime = datetime.datetime.now()
        calculated_weight = round(hx_creatine.get_weight_mean(20) - casecreatineweight, 2)
        
        # Check if the calculated weight is below -100
        if calculated_weight >= -100:
            creatineweight = calculated_weight
            print(f"Creatine Weight: {creatineweight} at {current_datetime}")
            create_historiek = DataRepository.create_historiek(idcreateineweight, userid, current_datetime, creatineweight, 'creatine weight')
            if create_historiek:
                print('New history entry created successfully.')
            socketio.emit('B2F_creatineweight', {'weight': creatineweight})
        else:
            print(f"Invalid creatine weight value: {calculated_weight}, not updating creatineweight.")
    except Exception as e:
        print(f'Creatine weight error: {e}')



def read_sensors():
    GPIO.setmode(GPIO.BCM)  # Ensure correct pin numbering mode within the thread
    start_time = time.time()
    print('**** Reading sensorssssss ****')
    while not stop_threads:
        print('sending data')
        send_data_watersensor()
        send_data_bottlesensor()
        send_data_proteinweight()
        send_data_creatineweight()


def start_thread():
    thread = threading.Thread(target=read_sensors)
    thread.start()
    return thread


def my_callback_one(channel):
    start_time = time.time()
    while GPIO.input(btn) == GPIO.LOW:
        time.sleep(0.1)

    press_duration = time.time() - start_time


    if press_duration >= 2:
        print('Button pressed for 1 second or more! Shutting down...')
        os.system("sudo shutdown -h now")
    else:
        print('Button pressed but not long enough. Ignored.')


GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(btn, GPIO.FALLING, bouncetime=200)
GPIO.add_event_callback(btn, my_callback_one)

if __name__ == '__main__':
    try:
        watersensor = HC_SR04(trig1, echo1)
        bottlesensor = HC_SR04(trig2, echo2)
        
        Proteinmotor = StepperMotor([6, 13, 19, 26])
        Creatinemotor = StepperMotor([5, 17, 27, 22])

        waterpump = Waterpump(wp_pin)

        pcf = PCF(sda, scl, adres)
        lcd = LCD(rs, enable, pcf)
        lcd.clear_display()
        ips = check_output(['hostname', '--all-ip-addresses']).decode() #decode: bytes -> string
        ip_list = ips.split()
        if ip_list:
            ip_address = ip_list[0]  # Neem het eerste IP-adres
        else:
            ip_address = "No IP address"  # Fallback als er geen IP-adres is
        
        lcd.clear_display()
        lcd.write_message(ip_address)  # Schrijf het IP-adres naar het LCD
        rotary = rotaryEncoder(rot_switch, rot_dt, rot_clk, lcd, waterpump, Proteinmotor, Creatinemotor)

        hx_protein = HX711(dout_pin=hx1_dt, pd_sck_pin=hx1_clck)
        hx_creatine = HX711(dout_pin=hx2_dt, pd_sck_pin=hx2_clck)

        swap_file_creatine = '/home/user/2023-2024-projectone-mct-YoranWandelsStudentHowest/creatine.swp'
        if os.path.isfile(swap_file_creatine):
            with open(swap_file_creatine, 'rb') as swap_file:
                hx_creatine = pickle.load(swap_file)
                print('creatine')

        swap_file_protein = '/home/user/2023-2024-projectone-mct-YoranWandelsStudentHowest/protein.swp'
        if os.path.isfile(swap_file_protein):
            with open(swap_file_protein, 'rb') as swap_file:
                hx_protein = pickle.load(swap_file)
            print('protein')
        else:
            print('no protein')

        thread = start_thread()
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("Stopping threads and cleaning up GPIO")
        stop_threads = True
        thread.join()  # Ensure the thread has completed before cleaning up GPIO
        GPIO.cleanup()
