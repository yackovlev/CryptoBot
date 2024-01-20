import telebot
from config import TOKEN, keys
from utils import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_and_help(message: telebot.types.Message):
    text = 'Добро пожаловать в *CryptoCurrencyRates* бот! \n\nОн позволяет осуществить переводы курсов криптовалют и ' \
           'фиатных валют в любых доступных парах.\n\nСписок доступных для конвертации валют: /values \nПри ' \
           'использовании десятичных дробей (актуально для BTC) используйте знак точки\n\nЧтобы ' \
           'начать работу введите команду в следующем формате: \n_<Тикер валюты 1> <Тикер валюты 2> <Сумма>_ \n\n ' \
           'Например, USD RUB 100 '
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для конвертации валюты: \n'
    for key in keys.keys():
        text = ''.join((text, key, ' | '))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_convert = message.text.split(' ')
        if len(values_convert) != 3:
            raise ConvertionException('Задано неверное количество параметров для вычисления')
        quote, base, amount = values_convert
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка! {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка! Не удалось обработать команду \n{e}')
    else:
        text = f'Стоимость {amount} {quote} - {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
