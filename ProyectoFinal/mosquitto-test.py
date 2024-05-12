import paho.mqtt.client as mqtt

def connectionStatus(client, userdata, flags, rc):
	mqttClient.subscribe("rpi/gpio")

def publish(message):
	result = mqttClient.publish("rpi/gpio", message)


def messageDecoder(client, userdata, msg):
	message = msg.payload.decode(encoding='UTF-8')
	if message == "accepted":
		publish("unloked")
	print(message)

clientName = "pythyton"
serverAdress = "localhost"

mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, clientName)
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

mqttClient.connect(serverAdress)
mqttClient.loop_forever()
