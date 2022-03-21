import telebot
from Config import keys, TOKEN
from extensions import ConvertionException, CurrencyConvecter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты цену которой он хочет узнать> \
<имя валюты в которой надо узнать цену первой валютыы>\
<количество первой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
     try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        if (quote != 'рубль') and (quote != 'доллар') and (quote != 'евро'):
            raise ConvertionException(f'Валюта {quote} отсутвует в списке')

        if (base != 'рубль') and (base != 'доллар') and (base != 'евро'):
            raise ConvertionException(f'Валюта {base} отсутвует в списке')

        total_base = CurrencyConvecter.get_price(quote, base, amount)

     except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
     except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду \n{e}')
     else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)