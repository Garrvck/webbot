from fastapi import UploadFile, Form, FastAPI
from fastapi.responses import FileResponse, JSONResponse

from tempfile import NamedTemporaryFile
import shutil
import os
ADMIN = 6728174283
from handlers.users.word import generate_resume_doc
from loader import bot

import uvicorn  # ✅ kerak
import threading  # ✅ botni fon rejimida ishlatish uchun

from aiogram import executor
from loader import dp
from utils.notify_admins import on_startup_notify
# from utils.set_bot_commands import set_default_commands
import json
app = FastAPI()


from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from PIL import Image, ExifTags

def fix_image_orientation(image_path):
    try:
        image = Image.open(image_path)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)

            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)

            image.save(image_path)
    except Exception as e:
        print("❌ Rasmni oriyentatsiyasini to'g'rilashda xatolik:", e)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
    dav_mukofoti: str = Form(""),
    deputat: str = Form(""),
    adresss: str = Form(""), # Yangi qator
    work_experience: str = Form(""),
    phone: str = Form(""),
    tg_id: str = Form(""),
    relatives: str = Form(...),   # bu JSON formatdagi string
    photo: UploadFile = None
):
    try:
        # ✅ Rasmni vaqtincha saqlaymiz
        photo_path = None
        if photo:
            with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                shutil.copyfileobj(photo.file, tmp)
                photo_path = tmp.name
            fix_image_orientation(photo_path)
        relatives_list = json.loads(relatives)  # str → list[dict]
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
            "dav_mukofoti": dav_mukofoti,
            "deputat": deputat,
            "adresss": adresss,
            "work_experience": work_experience,
            "phone": phone,
            "photo_path": photo_path,
            "from_user": {"id": tg_id},
            "relatives": relatives_list
        }

        # ✅ Word faylni yaratamiz
        docx_file = generate_resume_doc(resume_dict)

        # ✅ Telegramga yuboramiz
        await bot.send_document(int(tg_id), open(docx_file, "rb"), caption="✅ Sizning rezyume faylingiz tayyor!")
        await bot.send_document(
            ADMIN,
            open(docx_file, "rb"),
            caption=f"{tg_id}  tomonidan tayyorlangan rezyume"
        )
        return {"status": "success"}
        # # ✅ Foydalanuvchiga ham faylni qaytaramiz
        # return FileResponse(docx_file, filename="rezyume.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

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
        # await set_default_commands(dispatcher)
        await on_startup_notify(dispatcher)

    executor.start_polling(dp, on_startup=on_startup)


# ✅ Heroku uchun web-serverni ishga tushiramiz
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=port)
