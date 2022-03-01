import requests
import json
import telebot
import network

API_KEY = '5290869038:AAGiAc6P6TwTyJTb0YpGu_kv3MsucNWFRcw'
bot = telebot.TeleBot(API_KEY)

def check_if_correct(msg):
    return msg.text in ['campus', 'flex', 'falcon', 'swipe', 'Campus', 'Flex', 'Falcon', 'Swipe']

@bot.message_handler(func=check_if_correct)
def get_data(message):
    response = network.getMoney(message.text)
    ans = 'Balance: ' + response['balance'] + '\n\n'
    for transaction in response['transactions']:
        ans += transaction['date'] + ', ' + transaction['place'] + ', ' + transaction['chargedPrice'] + '\n'
    bot.reply_to(message, ans)
 
bot.polling()