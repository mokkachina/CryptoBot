import telebot
import requests
import json


TOKEN = '5442961952:AAF49j_26yusJRVxhrHpI6rbz-Xl38JsOmI'

bot = telebot.TeleBot(TOKEN)


keys = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'dollar': 'USD'
}
class ConvertionException(Exception):
    pass


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
   text = 'Введите команду боту на англиском : \n<имя валюты> \ ' \
          '<в какую валюту меняем> \
          <колличество валюты>\n Список валют: /values'
   bot.reply_to(message, text)
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
   text = 'Доступные валюты:'
   for key in keys.keys():
       text = '\n'.join((text,key))
   bot.reply_to(message, text)
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionException('Слишком много параметров.')

    quote, base, amount = values
    # quote_ticker, base_ticker = keys[quote], keys[base]
    if quote == base:
        raise ConvertionException(f'Не возможно конвертировать одинаковые валюты {base}.')
    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту{quote}.')
    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту{base}.')
    try:
        amount = float(amount)
    except KeyError:
        raise ConvertionException(f'Не удалось обработать колличество {amount}.')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {total_base} '
    bot.send_message(message.chat.id,text)


bot.polling()