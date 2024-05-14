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
    print(message)
    message_str = json.dumps(message)
    result = mqttClient.publish("rpi/gpio", message_str)
    


def connection_status(client, userdata, flags, rc):
    mqttClient.subscribe("rpi/gpio")

def message_decoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    print("mensaje: ")
    print(message)
    message_data = json.loads(message)
    modeSelection(message_data)

def open_door():
    print("Acceso Permitido")
    publish_message(MessageType.UNLOKED)


def id_verification():
        open_door()

def verification_failed():
    print("Acceso denegado")
    publish_message(MessageType.DENIED_ACCESS)

def remove_id():
        print("Key removed")
        publish_message(MessageType.REMOVED)

def addID():
    print("New key is stored")
    publish_message(MessageType.ADDED)

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
    
# setup the device

client_name = "doorController"
server_address = "localhost"

mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
mqttClient.on_connect = connection_status
mqttClient.on_message = message_decoder
mqttClient.connect(server_address)
mqttClient.loop_forever()
