import logging
from aiogram import types, Bot, Dispatcher, executor
from inline_btn import *
from database import *
from utils import translator_text

BOT_TOKEN = '6429806837:AAHvn4824gZdReWN-r61AjdYE1eN8YfSofU'
ADMINS = [5883851815]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot)


async def comand_menu(dp: Dispatcher):
    await create_tables()
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Ishga tushirish'),
            types.BotCommand('help', 'Ishga tushirish'),
            types.BotCommand('stat', 'Bot azolarini sonini korsatib beradi.')
        ]
    )


@dp.message_handler(commands=['start'])
async def get_start(message: types.Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer(f"Salom. Men Engu Tarjimon bot")


@dp.message_handler(commands=['stat'])
async def get_user_text_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        counts = await get_all_users()
        await message.answer(f"Bot azolari soni: {counts} ta")


@dp.message_handler(content_types=['text'])
async def get_user_text_handler(message: types.Message):
    btn = await translate_langs_btn()
    await message.answer(text=message.text, reply_markup=btn)


@dp.callback_query_handler(text_contains='lang')
async def selected_lang_callback(call: types.CallbackQuery):
    lang = call.data.split(':')[-1]
    text = call.message.text

    result_text = await translator_text(text=text, lang=lang)

    btn = await translate_langs_btn()
    await call.message.edit_text(text=result_text, reply_markup=btn)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=comand_menu)