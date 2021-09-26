from gpiozero import LED
from time import sleep

pump = LED(17)

while True:
    print('onnnnn')
    pump.off()
    sleep(3)
    print('offfffff')
    pump.on()
    sleep(1)
