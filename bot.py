import telebot
from telebot import types
from scat import skat

bot = telebot.TeleBot("5214157343:AAEkESKZid9umEo7L4PdCoJ-41m1clbCcM0")


@bot.message_handler(commands=["start"])
def start(message):
    text = """Здравствуйте, я так называемый Максим Инютин.\n\nДнём я обычный клоун, но ночью во мне просыпается настоящий python-программист. Тиран, гроссмейстер олимпроги пришёл, чтобы помочь начинающим падаванам Валентина Евгеньевича уничтожить дорешку и получить заветные баллы.\n\nОтправь боту код, полученный от твоего умного друга, и получи оплеуху -- решение, которое можно без малейшего мозгошевеления заслать на проверку."""
    bot.send_message(message.chat.id, text, parse_mode="html")


@bot.message_handler()
def go_skat(message):
    text = skat(message.text)
    bot.send_message(message.chat.id, text)



while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)