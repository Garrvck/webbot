from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from handlers.users.word import generate_resume_doc
from loader import dp, db, bot
from data.config import BOT_TOKEN, ADMINS
import requests


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove


user_data = {}  # user_id: resume_dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.dispatcher.filters import CommandStart
import requests

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    tg_id = message.from_user.id
    
    fullname = message.from_user.full_name
    webapp_url = f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"

    # ✅ Telegram chap menyudagi WebApp tugmasini olib tashlash
    menu_clear_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"
    requests.post(menu_clear_url, json={"menu_button": {"type": "default"}})

    # ✅ Inline tugma (chat ichida)
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📄 Rezyumeni to‘ldirish", web_app=WebAppInfo(url=webapp_url))
    )
    # ✅ Foydalanuvchini bazaga qo‘shish
    user = db.select_user(tg_id=tg_id)
    if not user:
        db.add_user(tg_id, fullname)

        # ✅ Adminga xabar yuborish
        count, = db.count_users()
        await bot.send_document(
            ADMINS[0],
            InputFile("data/main.db"),
            caption=f"jami-{count}"
        )
    try:
        photo1 = InputFile("data/pic1.jpg")
        await message.answer_photo(photo1)
    except:
        pass

    try:
        photo2 = InputFile("data/pic2.jpg")
        await message.answer_photo(photo2)
    except:
        pass
    # ✅ Xabar yuborish
    await message.answer(
        "👋 Assalomu alaykum!\n📄 Rezyume (ma’lumotnoma)\n✅ Tez\n✅ Oson\n✅ Ishonchli \nto‘ldirish uchun 🌐 web sahifaga o'ting",
        reply_markup=keyboard
    )

# @dp.message_handler(Command("start_resume"))
# async def start_resume_handler(message: types.Message):
#     tg_id = message.from_user.id
#     url = f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"
#     await message.answer(f"👇 Rezyume to‘ldirish uchun sahifani oching:\n{url}", reply_markup=ReplyKeyboardRemove())

