from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command

from handlers.users.word import generate_resume_doc
from loader import dp
from data.config import BOT_TOKEN
import requests


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove


user_data = {}  # user_id: resume_dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.dispatcher.filters import CommandStart
import requests

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    tg_id = message.from_user.id
    await message.answer("👋 Assalomu alaykum!", reply_markup=ReplyKeyboardRemove())
    url = f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"

    # Inline tugma orqali rezyume yuborish
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📄 Rezyumeni to‘ldirish", web_app=WebAppInfo(url=url))
    )

    # # Chat menyusiga ham Web App tugmasi qo‘shamiz
    # set_menu_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"
    # data = {
    #     "menu_button": {
    #         "type": "web_app",
    #         "text": "📄 Ma'lumotnoma",
    #         "web_app": {
    #             "url": url
    #         }
    #     }
    # }
    # requests.post(set_menu_url, json=data)

    # Xabar yuboramiz
    await message.answer(
        "📄 Rezyume (ma’lumotnoma) to‘ldirish uchun tugmani bosing:",
        reply_markup=keyboard
    )


# @dp.message_handler(Command("start_resume"))
# async def start_resume_handler(message: types.Message):
#     tg_id = message.from_user.id
#     url = f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"
#     await message.answer(f"👇 Rezyume to‘ldirish uchun sahifani oching:\n{url}", reply_markup=ReplyKeyboardRemove())

