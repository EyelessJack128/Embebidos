from gpiozero import RGBLED, Motor
from pn532_repo.pn532.api import PN532
from colorzero import Color
from time import sleep
from enum import Enum
import paho.mqtt.client as mqtt
import json

class MessageType(Enum):
    #envíos
    VERIFIEDFID = "verifiedFID"
    DENIEDFID = "deniedFID"
    ADD = "add"
    REMOVE = "remove"
    ##respuestas
    UNLOKED = "unloked"
    REMOVED = "removed"
    ADDED = "added"
    DENIED_ACCESS = "access_denied"

#{
#    type: "verifiedFID"
#}

def connectionStatus(client, userdata, flags, rc):
    mqttClient.subscribe("rpi/gpio")

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    message_data = json.loads(message)
    modeSelection(message_data)

def openDoor():
    print("Acceso Permitido")
    led.color = Color('green')
    motor.forward()
    sleep(3)
    motor.stop()
    sleep(3)
    motor.backward()
    sleep(3)

led = RGBLED(17, 27, 22)
validIDs =[[1, 0, 4, 8, 4, 227, 217, 5, 148, 121,0]]
motor = Motor(forward=4, backward=14)

def idVerification():
    led.color = Color('blue')
    read = nfc.read()
    led.off()
    mesaggeConfirmation = False
    for validID in validIDs:
        if validID == read:
            mesaggeConfirmation = True
            break
        else:
            mesaggeConfirmation = False

    if mesaggeConfirmation:
        openDoor()
    else:
        verification_failed()

def verification_failed():
    print("Acceso denegado")
    led.color = Color('red')
    sleep(2)
    led.off()

def removeID():
    led.color = Color('red')
    read = nfc.read()
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

def addID():
    led.color = Color('yellow')
    read = nfc.read()
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

def modeSelection(message_data: dict):
    message_type = message_data["type"]
    if message_type == MessageType.ADD.value:
        addID()
    elif message_type == MessageType.REMOVE.value:
        removeID()
    elif message_type == MessageType.VERIFIEDFID.value:
        
        idVerification()
    elif message_type == MessageType.DENIEDFID.value:
        verification_failed()
    else:
        print("Mensaje no reconocido")
    
nfc = PN532()
# setup the device
nfc.setup(enable_logging=False)

clientName = "doorController"
serverAdress = "localhost"

mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, clientName)
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder
mqttClient.connect(serverAdress)
mqttClient.loop_forever()
