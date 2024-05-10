#!/usr/bin/python3

from pn532.api import PN532
from gpiozero import LED, Servo
from time import sleep

led = LED(16)
servoState = False


if __name__== "__main__":
    nfc = PN532()

    # setup the device
    nfc.setup(enable_logging=False)

    # keep reading until a value is returned
    while True:
        read = nfc.read()
        print(read)
        led.on()
        sleep(2)
        led.off()
        


