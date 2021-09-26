import time
import Adafruit_ADS1x15


adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

while True:
    val = adc.read_adc(0, gain=GAIN)
    print(val)
    time.sleep(1)
