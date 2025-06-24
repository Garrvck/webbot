from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command
# from data.config import OPENAI_KEY
from handlers.users.word import generate_resume_doc
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")

@dp.message_handler(Command("start_resume"))
async def start_resume_handler(message: types.Message):
    html_link = "https://resume-bot-cfc4560e271d.herokuapp.com/"
    await message.answer(
        f"📝 Rezyume to‘ldirish uchun quyidagi havolaga o'ting:\n\n<a href='{html_link}'>➡️ Formani to‘ldirish</a>",
        disable_web_page_preview=True
    )

