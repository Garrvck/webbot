from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")

@dp.message_handler(Command("start_resume"))
async def start_resume_handler(message: types.Message):
    tg_id = message.from_user.id
    url = f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"
    await message.answer(f"👇 Rezyume to‘ldirish uchun sahifani oching:\n{url}")
