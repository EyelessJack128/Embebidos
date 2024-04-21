#!/usr/bin/python

import telebot

API_TOKEN='6950964391:AAEX280Xhu6MjelHcIj5lvoDVyTARZbo3D4'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exactly
    """)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message,message.text)

bot.polling()