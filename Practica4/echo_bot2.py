#!/usr/bin/python

import os
from gpiozero import LED
import telebot

led= LED(17)

API_TOKEN='6950964391:AAEX280Xhu6MjelHcIj5lvoDVyTARZbo3D4'
bot=telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['apaga'])
def turn_off(message):
    led.off()
    bot.reply_to(message,"""\
    se apago\
    """)

@bot.message_handler(commands=['enciende'])
def turn_on(message):
    led.on()
    bot.reply_to(message,"""\
    se encendio\
    """)

bot.polling()