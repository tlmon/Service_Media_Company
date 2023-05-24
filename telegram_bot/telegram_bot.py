from telegram_token import token # telegram bot token
import telebot
from telebot import types
from messages import get_trends_message, get_insights_message

bot = telebot.TeleBot(token, parse_mode=None) 


@bot.message_handler(commands=['start'])
def start(message):
    button_trends = types.KeyboardButton("Тренды")
    button_insigths = types.KeyboardButton("Инсайты")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button_trends)
    markup.add(button_insigths)
    
    part1 = "Что вы хотите получить?"
    part2 = "\nТренд - это долгосрочный (180 дней) объект обсуждения или направление развития."
    part3 = "\nИнсайт - это краткосрочное (до 3 дней) событие или открытие, которое предоставляет новую информацию."
    message_text = part1 + part2 + part3

    bot.send_message(message.from_user.id, message_text, reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    wait_mesage_text = 'Ваш запрос обрабатывается, подождите...'
    if message.text=="Тренды":
        wait_mesage = bot.send_message(message.chat.id, wait_mesage_text)
        trends = get_trends_message()
        bot.delete_message(message.chat.id, wait_mesage.message_id)
        bot.send_message(message.chat.id, trends)
    elif message.text=="Инсайты":
        wait_mesage = bot.send_message(message.chat.id, wait_mesage_text)
        insights = get_insights_message()
        bot.delete_message(message.chat.id, wait_mesage.message_id)
        bot.send_message(message.chat.id, insights)
    else:
        error_text = 'Неизвестная команда. Используйте кнопки для запроса.'
        bot.send_message(message.chat.id, error_text)

if __name__ == '__main__':
    bot.infinity_polling()
