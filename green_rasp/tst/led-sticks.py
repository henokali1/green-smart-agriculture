import qwiic_led_stick
import time

def light_on():
    my_stick = qwiic_led_stick.QwiicLEDStick()
    # Turn on all the LEDs to white
    my_stick.set_all_LED_color(220,20,60)


def light_off():
    my_stick = qwiic_led_stick.QwiicLEDStick()
    # Turn off all LEDs
    my_stick.LED_off()


light_on()
time.sleep(5)
light_off()

