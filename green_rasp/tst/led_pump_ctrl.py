import qwiic_led_stick
import qwiic_relay
import time
import urllib.request
import json


stat_url = 'http://18.117.252.6:8888/act_stat'

def light_on():
    print('light on')
    my_stick = qwiic_led_stick.QwiicLEDStick()
    # Turn on all the LEDs to white
    my_stick.set_all_LED_color(50, 50, 50)


def light_off():
    print('light off')
    my_stick = qwiic_led_stick.QwiicLEDStick()
    # Turn off all LEDs
    my_stick.LED_off()

def pump_on():
    print('Pump On')
    myRelays = qwiic_relay.QwiicRelay()
    myRelays.set_relay_on(1)

def pump_off():
    print('Pump Off')
    myRelays = qwiic_relay.QwiicRelay()
    myRelays.set_relay_off(0)

while 1:
    stat = json.loads(urllib.request.urlopen(stat_url).read().decode("utf-8"))
    # print(stat)
    light_on() if stat['light_on'] else light_off()
    pump_on () if stat['pump_on'] else pump_off()
    time.sleep(1)