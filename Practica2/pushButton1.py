from gpiozero import Button
from time import sleep
button = Button(2)
while True:
	if button.is_pressed:
		print("Button is pressed")
	else:
		print("Button is not pressed")
	sleep(1)
