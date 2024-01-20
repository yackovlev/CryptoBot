import telebot
from config import TOKEN, keys
from utils import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_and_help(message: telebot.types.Message):
    text = 'Добро пожаловать в бот! \n Список доступных валют: /values \n Чтобы начать работу введите команду в следующем формате: <имя исходной валюты> <имя валюты для перевода> <сумма>'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Задано неверное число параметров для вычисления')
        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Стоимость {amount} {quote} - {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
