from aiogram import Bot, Dispatcher, executor, types
from db import find_in_db, insert_user_db
from scat import go_skat
from mail import send_message
import time
import os


KEY_TG = os.environ.get('KEY_TG')
bot = Bot(token=KEY_TG)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    if not find_in_db(message.from_user.id):
        _id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        insert_user_db(_id, first_name, last_name)
        text_for_email = f"{first_name} {last_name} logged"
        await send_message(text_for_email)
    text = """Здравствуйте, я так называемый Максим Инютин.\n\nДнём я обычный клоун, но ночью во мне просыпается настоящий python-программист. Тиран, гроссмейстер олимпроги пришёл, чтобы помочь начинающим падаванам Валентина Евгеньевича уничтожить дорешку и получить заветные баллы.\n\nОтправь боту код, полученный от твоего умного друга, и получи оплеуху -- решение, которое можно без малейшего мозгошевеления заслать на проверку."""
    await message.answer(text)


@dp.message_handler()
async def go_sсat(message: types.Message):
    text = go_skat(message.text)
    text_for_email = f"Дружище {message.from_user.first_name} {message.from_user.last_name} скатывает задачу:\n\n{text}"
    await send_message(text_for_email)
    await message.answer(text)


while True:
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        time.sleep(15)