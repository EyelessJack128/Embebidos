from gpiozero import LEDBoard
from time import sleep
from signal import pause
from bluedot import BlueDot

def print_letter(letter: list):
    leds = LEDBoard(14, 15, 18, 23, 24, 25, 8)
    leds.on()
    leds.value = tuple(letter)
    sleep(1)

names = [
   [ 
        [1,1,1,1,0,1,0], #R
        [1,1,1,1,0,0,1], #I
        [0,1,1,0,0,0,1], #C
        [0,0,0,1,0,0,0], #A
        [1,1,1,1,0,1,0], #R
        [1,0,0,0,0,1,0], #D
        [0,0,0,0,0,0,1]  #O
   ],
   [
        [1,0,0,0,1,1,1], #J
        [0,1,1,0,0,0,0], #E
        [0,1,0,0,1,0,0], #S
        [1,0,0,0,0,0,1], #U
        [0,1,0,0,1,0,0]  #S
   ],
   [
        [0,1,1,0,0,0,0], #E
        [1,0,0,0,0,1,0], #D
        [1,0,0,0,0,0,1], #U
        [0,0,0,1,0,0,0], #A
        [1,1,1,1,0,1,0], #R
        [1,0,0,0,0,1,0], #D
        [0,0,0,0,0,0,1]  #O
   ],
   [
        [0,1,0,0,0,0,0], #G
        [1,0,0,0,0,0,1], #U
        [0,0,0,1,0,0,0], #A
        [1,0,0,0,0,1,0], #D
        [0,0,0,1,0,0,0], #A
        [1,1,1,0,0,0,1], #L
        [1,0,0,0,0,0,1], #U
        [0,0,1,1,0,0,0], #P
        [0,1,1,0,0,0,0]  #E
   ]
]

def selectedName(listNum : int):
    name = names[listNum]
    for a in name:
        print_letter(a)

def dpad(pos):
    if pos.top:
        selectedName(0)
    elif pos.bottom:
        selectedName(1)
    elif pos.left:
        selectedName(2)
    elif pos.right:
        selectedName(3)

bd = BlueDot()
bd.when_pressed = dpad

pause()
    







