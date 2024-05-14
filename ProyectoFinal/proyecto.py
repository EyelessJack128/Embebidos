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

def publish_message(type: MessageType):
    message = {"type": ""}
    if type == MessageType.UNLOKED:
        message["type"] = MessageType.UNLOKED.value
    elif type == MessageType.REMOVED:
        message["type"] = MessageType.REMOVED.value
    elif type == MessageType.ADDED:
        message["type"] = MessageType.ADDED.value
    elif type == MessageType.DENIED_ACCESS:
        message["type"] = MessageType.DENIED_ACCESS.value
    else:
        message["type"] = "error_message"
    message_str = json.dumps(message)
    result = mqttClient.publish("rpi/gpio", message_str)
    


def connection_status(client, userdata, flags, rc):
    mqttClient.subscribe("rpi/gpio")

def message_decoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    message_data = json.loads(message)
    modeSelection(message_data)

def open_door():
    print("Acceso Permitido")
    led.color = Color('green')
    publish_message(MessageType.UNLOKED)
    motor.forward()
    sleep(3)
    motor.stop()
    sleep(3)
    motor.backward()
    sleep(3)

led = RGBLED(17, 27, 22)
valid_ids =[[1, 0, 4, 8, 4, 227, 217, 5, 148, 121,0]]
motor = Motor(forward=4, backward=14)

def id_verification():
    led.color = Color('blue')
    read = nfc.read()
    led.off()
    mesagge_confirmation = False
    for valid_id in valid_ids:
        if valid_id == read:
            mesagge_confirmation = True
            break
        else:
            mesagge_confirmation = False

    if mesagge_confirmation:
        open_door()
    else:
        verification_failed()

def verification_failed():
    print("Acceso denegado")
    led.color = Color('red')
    publish_message(MessageType.DENIED_ACCESS)
    sleep(2)
    led.off()

def remove_id():
    led.color = Color('red')
    read = nfc.read()
    led.off()
    if read in valid_ids:
        valid_ids.remove(read)
        print("Key removed")
        led.color = Color('green')
        publish_message(MessageType.REMOVED)
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
    if read in valid_ids:
        print("Key is already stored")
        led.color = Color('red')
        sleep(0.5)
        led.off()
    else:
        valid_ids.append(read)
        print("New key is stored")
        led.color = Color('green')
        publish_message(MessageType.ADDED)
        sleep(0.5)
        led.off()
    sleep(0.5)

def modeSelection(message_data: dict):
    message_type = message_data["type"]
    if message_type == MessageType.ADD.value:
        addID()
    elif message_type == MessageType.REMOVE.value:
        remove_id()
    elif message_type == MessageType.VERIFIEDFID.value:
        id_verification()
    elif message_type == MessageType.DENIEDFID.value:
        verification_failed()
    else:
        print("Mensaje no reconocido")
    
nfc = PN532()
# setup the device
nfc.setup(enable_logging=False)

client_name = "doorController"
server_address = "localhost"

mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
mqttClient.on_connect = connection_status
mqttClient.on_message = message_decoder
mqttClient.connect(server_address)
mqttClient.loop_forever()
