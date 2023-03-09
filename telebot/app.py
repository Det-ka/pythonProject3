
import telebot
from TOKEN import keys, TOKEN
from exception import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


# Приветствие, инструкция.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы узнать актуальный курс, введите комманду в следующем формате: \
\n<Имя вашей валюты> \
<Имя валюты в которую хотите перевести> \
<Количество переводимой валюты> \nСписок всех доступных валют: /values'
    bot.reply_to(message, text)


# обработчики условий
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# API декоратор
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except CryptoConverter as e:
        bot.reply_to(message,f'Ошибка пользователяю.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
