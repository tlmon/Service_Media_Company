from telegram_token import token # telegram bot token
import telebot
from telebot import types
import requests as rq
import json


bot = telebot.TeleBot(token, parse_mode=None) 

@bot.message_handler(commands=['start', 'help', 'info'])
def start(message):
    button_trends = types.KeyboardButton("Тренды")
    button_insigths = types.KeyboardButton("Инсайты")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button_trends)
    markup.add(button_insigths)
    
    bot.send_message(message.from_user.id, "Что вы хоитите получить?", reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Тренды":
        mes = bot.send_message(message.chat.id, 'Ваш запрос оборобатывается, подождите...')
        bot.delete_message(message.chat.id, mes.message_id)
        bot.send_message(message.chat.id, get_trends())
    elif message.text=="Инсайты":
        bot.send_message(message.chat.id, 'Ваш запрос оборобатывается, подождите...')
        bot.send_message(message.chat.id, get_insights())

def get_trends():
    response = rq.get('http://127.0.0.1:8080/api/v0/trends')
    if response.status_code != 200:
        return "Произошла ошибка. Попробуйте позже..."

    result = "Тренды:\n"
    number = 1     
    for trend in json.loads(response.text)[:10]:
        result += str(number) + '. ' + trend['trend'] + '\n'
        number += 1
    return result

def get_insights():
    response = rq.get('http://127.0.0.1:8080/api/v0/insights')
    if response.status_code != 200:
        return "Произошла ошибка. Попробуйте позже..."

    result = "Инсайты:\n"
    number = 1     
    for insight in json.loads(response.text)[:10]:
        result += str(number) + '. ' + str.replace(insight['insight'], '\n', '') + '\n'
        number += 1
    return result


def main():
    print('Start telegram bot')

    bot.infinity_polling()


if __name__ == '__main__':
    main()
