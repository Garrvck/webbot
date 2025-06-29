from fastapi import UploadFile, Form, FastAPI
from fastapi.responses import FileResponse, JSONResponse

from tempfile import NamedTemporaryFile
import shutil
import os

from handlers.users.word import generate_resume_doc
from loader import bot

import uvicorn  # ✅ kerak
import threading  # ✅ botni fon rejimida ishlatish uchun

from aiogram import executor
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

app = FastAPI()


@app.post("/send_resume_data")
async def receive_resume(
    full_name: str = Form(...),
    birth_date: str = Form(""),
    birth_place: str = Form(""),
    nationality: str = Form(""),
    party_membership: str = Form(""),
    education: str = Form(""),
    university: str = Form(""),
    specialization: str = Form(""),
    ilmiy_daraja: str = Form(""),
    ilmiy_unvon: str = Form(""),
    languages: str = Form(""),
    deputat: str = Form(""),
    dav_mukofoti: str = Form(""),
    work_experience: str = Form(""),
    phone: str = Form(""),
    tg_id: str = Form(""),
    photo: UploadFile = None
):
    try:
        # ✅ Rasmni vaqtincha saqlaymiz
        photo_path = None
        if photo:
            with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                shutil.copyfileobj(photo.file, tmp)
                photo_path = tmp.name

        # ✅ Ma’lumotlarni tayyorlaymiz
        resume_dict = {
            "full_name": full_name,
            "birth_date": birth_date,
            "birth_place": birth_place,
            "nationality": nationality,
            "party_membership": party_membership,
            "education": education,
            "university": university,
            "specialization": specialization,
            "ilmiy_daraja": ilmiy_daraja,
            "ilmiy_unvon": ilmiy_unvon,
            "languages": languages,
            "deputat": deputat,
            "dav_mukofoti": dav_mukofoti,
            "work_experience": work_experience,
            "phone": phone,
            "photo_path": photo_path,
            "from_user": {"id": tg_id}
        }

        # ✅ Word faylni yaratamiz
        docx_file = generate_resume_doc(resume_dict)

        # ✅ Telegramga yuboramiz
        await bot.send_document(int(tg_id), open(docx_file, "rb"))

        # ✅ Foydalanuvchiga ham faylni qaytaramiz
        return FileResponse(docx_file, filename="rezyume.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
        if 'docx_file' in locals() and os.path.exists(docx_file):
            os.remove(docx_file)


# ✅ Telegram botni fon rejimida ishga tushiramiz
def start_bot():
    async def on_startup(dispatcher):
        await set_default_commands(dispatcher)
        await on_startup_notify(dispatcher)

    executor.start_polling(dp, on_startup=on_startup)


# ✅ Heroku uchun web-serverni ishga tushiramiz
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=port)
