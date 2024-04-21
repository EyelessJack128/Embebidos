import os
from gpiozero import LED, MotionSensor
import telebot
from signal import pause

led= LED(17)
pir = MotionSensor(27)
chatID = 1240537910

API_TOKEN='6950964391:AAEX280Xhu6MjelHcIj5lvoDVyTARZbo3D4'
bot=telebot.TeleBot(API_TOKEN)

def turn_off(message):
    led.off()

def turn_on(message):
    led.on()
    bot.send_message(chatID, "Persona detectada")

pir.when_motion = turn_on
pir.when_no_motion = turn_off
bot.polling()
pause()