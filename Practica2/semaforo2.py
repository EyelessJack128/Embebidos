from gpiozero import LED
import time
from gpiozero import Button

red = LED(17)
yellow = LED(27)
green = LED(22)
button = Button(2)

while True:
	green.on()
	time_start = time.time()
	while time.time() < time_start + 5:
		if button.is_pressed:
			print("Pressed")
			break
	green.off()
	green.blink(on_time=1,off_time=1,n=3,background=False)
	yellow.on()
	time.sleep(2)
	yellow.off()
	red.on()
	time.sleep(5)
	red.off()
