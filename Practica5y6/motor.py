from gpiozero import Motor
from time import sleep

motor = Motor(forward=4, backward=14)

while True:
    print("Avanzando")
    motor.forward()
    sleep(5)
    print("Retrocediendo")
    motor.backward()
    sleep(5)