from aiogram.types import ContentType
import sqlite3
import os
from aiogram import types
from data.config import ADMINS
from loader import dp



@dp.message_handler(content_types=ContentType.DOCUMENT)
async def handle_merge_db(message: types.Message):
    if message.from_user.id != ADMINS[0]:
        return await message.answer("⛔ Sizda ruxsat yo‘q")

    document = message.document
    if document.file_name != "main.db":
        return await message.answer("❗ Iltimos, faqat 'main.db' faylini yuboring.")

    temp_path = "temp_main.db"
    await document.download(destination_file=temp_path)

    try:
        # 🔄 Ikkita bazani ochamiz
        current_conn = sqlite3.connect("main.db")
        backup_conn = sqlite3.connect(temp_path)

        current_cursor = current_conn.cursor()
        backup_cursor = backup_conn.cursor()

        # 🔍 Zaxiradagi barcha foydalanuvchilarni olib kelamiz
        backup_cursor.execute("SELECT tg_id, fullname FROM Users")
        users = backup_cursor.fetchall()

        added = 0
        for tg_id, fullname in users:
            # Mavjudmi tekshiramiz
            current_cursor.execute("SELECT 1 FROM Users WHERE tg_id = ?", (tg_id,))
            if not current_cursor.fetchone():
                current_cursor.execute(
                    "INSERT INTO Users (tg_id, fullname) VALUES (?, ?)", (tg_id, fullname)
                )
                added += 1

        current_conn.commit()
        current_conn.close()
        backup_conn.close()

        os.remove(temp_path)  # vaqtincha faylni o‘chiramiz

        await message.answer(f"✅ Bazaga {added} ta yangi foydalanuvchi qo‘shildi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
