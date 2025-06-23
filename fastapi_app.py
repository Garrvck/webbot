from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from loader import bot
from handlers.users.word import generate_resume_doc

app = FastAPI()


from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send_resume_data")
async def receive_resume(request: Request):
    try:
        data = await request.json()
        chat_id = data.get("from_user", {}).get("id")

        if not chat_id:
            return JSONResponse(content={"error": "contact (Telegram ID) kerak"}, status_code=400)

        # ✅ Matnli xabar tayyorlash
        message = f"<b>📄 Yangi rezyume:</b>\n\n"
        message += f"<b>Ism:</b> {data.get('full_name')}\n"
        message += f"<b>Tug‘ilgan sana:</b> {data.get('birth_date')}\n"
        message += f"<b>Mutaxassisligi:</b> {data.get('specialization')}\n"

        if data.get("relatives"):
            message += "\n<b>Yaqin qarindoshlari:</b>\n"
            for idx, rel in enumerate(data["relatives"], 1):
                message += f"{idx}. {rel.get('relation_type', '')}, {rel.get('full_name', '')}, {rel.get('b_year_place', '')}, {rel.get('job_title', '')}, {rel.get('address', '')}\n"

        # ✅ Matnni yuborish
        await bot.send_message(chat_id, message)

        # ✅ Word faylni yaratish va yuborish
        filename = generate_resume_doc(data)
        with open(filename, "rb") as doc_file:
            await bot.send_document(chat_id, doc_file)

        return {"status": "success"}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
