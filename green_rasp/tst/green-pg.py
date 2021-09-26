from __future__ import print_function
import Adafruit_ADS1x15
import urllib.request
import qwiic_bme280
from time import *
from gps import *
import threading
import glob
import time
import sys
import os
import qwiic_led_stick
from gpiozero import LED
# import qwiic_relay
import json
import requests
import pickle


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
stat_url = 'http://34.122.102.91:8888/act_stat'

mySensor = qwiic_bme280.QwiicBme280()
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
soil_moisture_treshold = 30
pump = LED(17)
pump.on()


if mySensor.connected == False:
    print("The Qwiic BME280 device isn't connected to the system. Please check your connection", file=sys.stderr)

mySensor.begin()

 
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 

def read_pickle_file(fn):
    with open(fn, 'rb') as handle:
        val = pickle.load(handle)
    return val

fn = '/home/pi/key/one_sig_creds.pickle'
creds = read_pickle_file(fn)

header = {"Content-Type": "application/json; charset=utf-8", "Authorization": creds['authorization']}
pump_on_payload = {"app_id": creds['app_id'], "included_segments": ["Subscribed Users"], "contents": {"en": "Water Sprinkler Switched On"}, "headings": {"en": "💦"}, "priority": 10}
pump_off_payload = {"app_id": creds['app_id'], "included_segments": ["Subscribed Users"], "contents": {"en": "Water Sprinkler Switched Off"}, "headings": {"en": "💦"}, "priority": 10}
lights_on_payload = {"app_id": creds['app_id'], "included_segments": ["Subscribed Users"], "contents": {"en": "Lights Switched On"}, "headings": {"en": "💡"}, "priority": 10}
lights_off_payload = {"app_id": creds['app_id'], "included_segments": ["Subscribed Users"], "contents": {"en": "Lights Switched Off"}, "headings": {"en": "💡"}, "priority": 10}
pump_notification_sent = False
lights_notification_sent = False
thread_running = True
manual_ctrl = False

def send_push_notification(val):
    return requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(val))

def read_soil_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_soil_temp():
    lines = read_soil_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_soil_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return round(temp_c, 2)


def light_on():
    print('light on')
    my_stick = qwiic_led_stick.QwiicLEDStick()
    # Turn on all the LEDs to white
    my_stick.set_all_LED_color(220,20,60)


def light_off():
    print('light off')
    my_stick = qwiic_led_stick.QwiicLEDStick()
    # Turn off all LEDs
    my_stick.LED_off()

def pump_on():
    print('Pump On')
    # myRelays = qwiic_relay.QwiicRelay()
    # myRelays.set_relay_on(1)
    pump.off()
    urllib.request.urlopen('http://34.122.102.91:8888/ctrl_act/?param=pump_on').read()
    time.sleep(.5)

def pump_off():
    print('Pump Off')
    # myRelays = qwiic_relay.QwiicRelay()
    # myRelays.set_relay_off(0)
    pump.on()
    urllib.request.urlopen('http://34.122.102.91:8888/ctrl_act/?param=pump_off').read()
    time.sleep(.5)


def thread_function(name):
    global pump_notification_sent
    global lights_notification_sent
    global manual_ctrl
    while thread_running:
        stat = json.loads(urllib.request.urlopen(stat_url).read().decode("utf-8"))
        manual_ctrl = stat['manual_ctrl']
        print(f"stat: {stat}")
        print(f'manual_ctrl: {manual_ctrl}')

        # Manual
        if((manual_ctrl) and (stat['light_on'])):
            light_on()
        if((manual_ctrl) and (not stat['light_on'])):
            light_off()
        if((manual_ctrl) and (stat['pump_on'])):
            pump_on()
        if((manual_ctrl) and (not stat['pump_on'])):
            pump_off()
        
        
        
        # Auto
        if ((manual_ctrl == False) and (stat['light_on']) and (lights_notification_sent == False)):
            light_on()
            send_push_notification(lights_on_payload)
            lights_notification_sent = True
        if ((manual_ctrl == False) and (not stat['light_on']) and (lights_notification_sent)):
            light_off()
            send_push_notification(lights_off_payload)
            lights_notification_sent = False


        if ((manual_ctrl == False) and (stat['pump_on']) and (pump_notification_sent == False)):
            pump_on()
            pump_notification_sent = True
            send_push_notification(pump_on_payload)
        if ((manual_ctrl == False) and (not stat['pump_on']) and (pump_notification_sent)):
            pump_off()
            send_push_notification(pump_off_payload)
            pump_notification_sent = False  
        time.sleep(1)

if __name__ == '__main__':
    gpsp = GpsPoller() # create the thread
    try:
        gpsp.start() # start it up
        ctrl_mntr = threading.Thread(target=thread_function, args=('index',))
        ctrl_mntr.start()
        while True:
            soil_temp = read_soil_temp()
            air_temp = round(mySensor.temperature_celsius,2)
            humidity = round(mySensor.humidity,2)
            air_pressure = round(mySensor.pressure,2)
            soil_moisture = adc.read_adc(0, gain=GAIN)
            soil_moisture = int(soil_moisture*100/26400)
            ldr = adc.read_adc(1, gain=GAIN)
            latitude = gpsd.fix.latitude
            longitude = gpsd.fix.longitude
            altitude = gpsd.fix.altitude
            
            formatted_vals = f'Soil Temp: {soil_temp}°C\tAir Temp: {air_temp}°C\t Humidity: {humidity}%\tPressure: {air_pressure}Pa\tSoil Moisture: {soil_moisture}\tLDR: {ldr}\tLat: {round(latitude,5)}\tLong: {round(longitude,5)}\tAlt: {altitude}m'
            # print(formatted_vals)
            url = f'http://34.122.102.91:8888/update_live_sensor_data/?soil_temp={soil_temp}&soil_moisture={soil_moisture}&air_temp={air_temp}&lat={round(latitude,5)}&lng={round(longitude,5)}'
            print(urllib.request.urlopen(url).read())
            # light_url = 'http://34.122.102.91:8888/ctrl_act/?param=light_on' if ldr < 3000 else 'http://34.122.102.91:8888/ctrl_act/?param=light_off'            
            if ((not manual_ctrl) and (ldr < 3000)):
                light_url = 'http://34.122.102.91:8888/ctrl_act/?param=light_on'
                urllib.request.urlopen(light_url).read()
            if ((not manual_ctrl) and (ldr > 3000)):
                light_url = 'http://34.122.102.91:8888/ctrl_act/?param=light_off' 
                urllib.request.urlopen(light_url).read()  
            # soil_moisture_url = 'http://34.122.102.91:8888/ctrl_act/?param=pump_on' if soil_moisture < soil_moisture_treshold else 'http://34.122.102.91:8888/ctrl_act/?param=pump_off'            
            if((not manual_ctrl) and (soil_moisture < soil_moisture_treshold)):
                soil_moisture_url = 'http://34.122.102.91:8888/ctrl_act/?param=pump_on'
                urllib.request.urlopen(soil_moisture_url).read()
                print('stat updated to: pump_on')
            if((not manual_ctrl) and (soil_moisture > soil_moisture_treshold)):
                soil_moisture_url = 'http://34.122.102.91:8888/ctrl_act/?param=pump_off'
                urllib.request.urlopen(soil_moisture_url).read()
                print('stat updated to: pump_off')
            
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit) as exErr:
        pump_off()
        light_off()
        print("\nKilling GPS Thread...")
        gpsp.running = False
        thread_running = False
        print("Killing Main Thread...")
        gpsp.join() # wait for the thread to finish what it's doing
print("Exiting.")
sys.exit(0)


