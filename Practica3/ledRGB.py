from bluedot import BlueDot
from gpiozero import PWMLED
from signal import pause

def set_brightness(pos):
    brightnessBlue = (pos.y + 1) / 2
    blueLed.value = brightnessBlue
    brightnessGreen = (pos.x + 1) / 2
    greenLed.value = brightnessGreen
    
blueLed = PWMLED(17)
greenLed = PWMLED(27)
redLed = PWMLED(22)
bd = BlueDot()
bd.when_moved = set_brightness

pause()