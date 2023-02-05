import telebot
from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def function_name(message: telebot.types.Message):
    text = 'Для работы с ботом введите команду следующим образом:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\
\nУвидеть весь список валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = f'\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        check = message.text.split(' ')

        if len(check) > 3:
            raise APIException('Слишком много параметров')
        if len(check) < 3:
            raise APIException('Слишком мало параметров')

        quote, base, amount = message.text.split(' ')

        quote = quote.lower()
        base = base.lower()

        ans = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {ans}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
