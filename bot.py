from aiogram import Bot, Dispatcher, executor, types
from scat import go_skat
import os

KEY_TG = os.environ.get('KEY_TG')
bot = Bot(token=KEY_TG)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    text = """Здравствуйте, я так называемый Максим Инютин.\n\nДнём я обычный клоун, но ночью во мне просыпается настоящий python-программист. Тиран, гроссмейстер олимпроги пришёл, чтобы помочь начинающим падаванам Валентина Евгеньевича уничтожить дорешку и получить заветные баллы.\n\nОтправь боту код, полученный от твоего умного друга, и получи оплеуху -- решение, которое можно без малейшего мозгошевеления заслать на проверку."""
    await message.answer(text)


@dp.message_handler()
async def go_sсat(message: types.Message):
    text = go_skat(message.text)
    await message.answer(text)


while True:
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        send_message(e)
        time.sleep(15)