from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command

from handlers.users.word import generate_resume_doc
from loader import dp




from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove


user_data = {}  # user_id: resume_dict

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")

@dp.message_handler(Command("start_resume"))
async def start_resume_handler(message: types.Message):
    tg_id = message.from_user.id
    url = f"https://resume-bot-cfc4560e271d.herokuapp.com/?id={tg_id}"
    await message.answer(f"👇 Rezyume to‘ldirish uchun sahifani oching:\n{url}", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(msg: types.Message):
    user_id = msg.from_user.id
    if user_id not in user_data:
        await msg.reply("❗ Avval rezyume ma’lumotlarini yuboring.")
        return

    photo = msg.photo[-1]  # eng katta o'lchamdagi rasm
    photo_path = f"{user_id}_photo.jpg"
    await photo.download(destination_file=photo_path)

    resume_dict = user_data.pop(user_id)  # ma’lumotni olamiz va o‘chirib yuboramiz
    resume_dict["photo_path"] = photo_path

    # Word fayl yaratamiz
    filename = generate_resume_doc(resume_dict)
    await msg.answer_document(open(filename, "rb"))

    # Fayllarni tozalash (ixtiyoriy)
    import os
    os.remove(photo_path)
    os.remove(filename)
