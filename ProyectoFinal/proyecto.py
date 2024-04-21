from gpiozero import RGBLED
from pn532_repo.pn532.api import PN532
from colorzero import Color
from signal import pause
from bluedot import BlueDot
from time import sleep

led = RGBLED(17, 27, 22)
validIDs =[[1, 0, 4, 8, 4, 227, 217, 5, 148, 121,0]]

def idVerification(read):
    led.off()
    mesaggeConfirmation = False
    for validID in validIDs:
        for a,b in zip(validID,read):
            if a != b:
                mesaggeConfirmation = False
                break
            else:
                mesaggeConfirmation = True
    if mesaggeConfirmation:
        print("Acceso Permitido")
        led.color = Color('green')
    else:
        print("Acceso Denegado")
        led.color = Color('red')
    sleep(2)
    led.off()

def removeID(read):
    led.off()
    if read in validIDs:
        validIDs.remove(read)
        print("Key removed")
        led.color = Color('green')
        sleep(0.5)
        led.off()
    else:
        print("Key not found")
        sleep(0.5)
        led.color = Color('red')
        sleep(0.5)
        led.off()
    sleep(0.5)

def addID(read):
    led.off()
    if read in validIDs:
        print("Key is already stored")
        led.color = Color('red')
        sleep(0.5)
        led.off()
    else:
        validIDs.append(read)
        print("New key is stored")
        led.color = Color('green')
        sleep(0.5)
        led.off()
    sleep(0.5)


def modeSelection(pos):
    if pos.top:
        led.color = Color('yellow')
        read = nfc.read()
        addID(read)
    elif pos.left:
        led.color = Color('red')
        read = nfc.read()
        removeID(read)
    elif pos.right:
        led.color = Color('blue')
        read = nfc.read()
        idVerification(read)
    sleep(0.5)

nfc = PN532()

# setup the device
nfc.setup(enable_logging=False)

bd = BlueDot()
bd.when_pressed = modeSelection

pause()
