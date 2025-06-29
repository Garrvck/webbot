from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command

from handlers.users.word import generate_resume_doc
from loader import dp
from data.config import BOT_TOKEN



from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove


user_data = {}  # user_id: resume_dict

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"
    tg_id = message.from_user.id
    data = {
        "menu_button": {
            "type": "web_app",
            "text": "📄 Mening Sahifam",
            "web_app": {
                "url": f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"  # bu yerga web sahifa linkini qo'ying
            }
        }
    }

    response = requests.post(url, json=data)
    print(response.json())
    await message.answer(f"Ma'lumotnoma tayyorlash botiga xush kelibsiz!")

@dp.message_handler(Command("start_resume"))
async def start_resume_handler(message: types.Message):
    tg_id = message.from_user.id
    url = f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"
    await message.answer(f"👇 Rezyume to‘ldirish uchun sahifani oching:\n{url}", reply_markup=ReplyKeyboardRemove())

