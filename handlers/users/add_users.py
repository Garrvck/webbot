from aiogram.types import ContentType
import sqlite3
import os
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot

ADMIN = 6728174283

@dp.message_handler(content_types=ContentType.DOCUMENT)
async def handle_merge_db(message: types.Message):
    if message.from_user.id != ADMIN:
        return await message.answer("⛔ Sizda ruxsat yo‘q")

    document = message.document
    if document.file_name != "main.db":
        return await message.answer("❗ Faqat 'main.db' nomli faylni yuboring.")

    temp_path = "temp_main.db"
    await document.download(destination_file=temp_path)

    try:
        # 🔄 Yangi (zaxira) bazani ochamiz
        backup_conn = sqlite3.connect(temp_path)
        backup_cursor = backup_conn.cursor()

        # 🔍 Jadval mavjudligini tekshiramiz
        backup_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
        if not backup_cursor.fetchone():
            backup_conn.close()
            os.remove(temp_path)
            return await message.answer("❌ 'Users' jadvali zaxira faylda topilmadi.")

        # 🔄 Barcha foydalanuvchilarni yuklaymiz
        backup_cursor.execute("SELECT tg_id, fullname FROM Users")
        users = backup_cursor.fetchall()
        backup_conn.close()
        os.remove(temp_path)

        added = 0
        for tg_id, fullname in users:
            before = db.count_users()[0]
            db.add_user(tg_id, fullname)
            after = db.count_users()[0]
            if after > before:
                added += 1

        await message.answer(f"✅ {added} ta foydalanuvchi qo‘shildi.")
        count, = db.count_users()
        await bot.send_document(
            ADMINS[0],
            InputFile("data/main.db"),
            caption=f"jami-{count}"
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
