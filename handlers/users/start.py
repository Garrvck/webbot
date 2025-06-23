from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

# from data.config import OPENAI_KEY
from handlers.users.word import generate_resume_doc
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")

#
# import asyncio
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import ParseMode
# from openai import AsyncOpenAI
#
# # API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# # OPENAI_KEY = "YOUR_OPENAI_API_KEY"
# #
# # bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
# # dp = Dispatcher()
# openai_client = AsyncOpenAI(api_key=OPENAI_KEY)
#
# # Har bir user uchun kontekst saqlanadi
# user_contexts = {}
# user_resume_dicts = {}
#
# # Boshlang‘ich GPT vazifasi (system prompt)
# SYSTEM_PROMPT = """
# Siz professional resume tuzuvchi sun’iy intellektsiz. Foydalanuvchidan suhbat orqali quyidagi ma’lumotlarni so‘rashingiz kerak:
#
# 1. full_name – To‘liq ism (malasan, Alijonov Valijon Shokir o'g'li, Abdullayeva Fotima Aziz qizi)
# 2. birth_date – Tug‘ilgan sana (01.01.2001-yil)
# 3. birth_place – Tug‘ilgan joy (Surxondaryo viloyati, Angor tumani, Nurafshon ko'chasi, 12-uy)
# 4. nationality – Millati
# 5. party_membership – Partiyaviyligi
# 6. education – Ma’lumoti
# 7. university – O‘qigan OTM (2015-2019 yillar. Toshkent Transport universiteti)
# 8. specialization – Mutaxassisligi
# 9. ilmiy_daraja – Ilmiy darajasi (ilmiy daraja, ilmiy unvon, depulatligi va davlat mukofoti bor yo'qligi jamlanib bir so'rovda so'ralsin)
# 10. ilmiy_unvon – Ilmiy unvoni
# 11. languages – Biladigan tillari
# 12. deputat – Deputatligi bor/yo‘qligi
# 13. dav_mukofoti – Davlat mukofotlari
# 14. work_experience – Mehnat faoliyati (tarixi, `Python dict` da foydalanuvchi aytgan har bir ish joyi yangi qatorda tire (-) bilan yozilishi kerak)
# 15. contact – Telefon raqami (masalan, +998 91 123 45 67 yoki 99 111 22 33)
# 16. photo_path – Rasmingiz (yo bo‘lmasa yozilsin)
#
# Shuningdek, har bir yaqin qarindosh (ota/ona/aka/opa/er/xotin/farzandlar) haqida quyidagilarni so‘rashingiz kerak:
#
# - relation_type: Kimligi (Masalan: ona)
# - full_name: To‘liq ism (malasan, Alijonov Valijon Shokir o'g'li, Abdullayeva Fotima Aziz qizi, Nuraliyev Sherali Shokirovich, Abdullayeva Fotima Azizovna)
# - b_year_place: Tug‘ilgan yili va joyi (masalan, 31.12.1977-yil, Jarqo'rg'on tumani)
# - job_title: Ish joyi va kasbi (masalan, Termiz shahar 12-maktab, O'qituvchi)
# - address: Yashash manzili (masalan, Surxondaryo viloyati, Angor tumani, Nurafshon ko'chasi, 12-uy)
#
# Qoida:
# - /start_resume bosganda "Assalomu alaykum, men resume yaratish AI botiman. Iltimos quyidagi savollarga javob bering!" deb boshlang. har bir savol alohida so'ralsin.
# - Har bir savolni alohida va izchil bering.
# - Javob yetarli bo‘lmasa aniqlashtiring.
# - Faqat zarur ma’lumotlarni yig‘ing.
# - Hech qanday izohsiz yakunlangach quyidagilarni bajaring:
#
# 1. Resume va qarindoshlar ma’lumotlarini bitta `Python dict` ko‘rinishida `json`ga o‘xshab chiqaring.
# 2. Izoh yozmang, faqat `dict` ni chiqaring.
# 3. Eng ohirida: “✅ Resume ma’lumotlari yig‘ildi. Fayl yarataymi?” deb so‘rang.
# """
#
#
# # Boshlash
# @dp.message_handler(commands=["start_resume"])
# async def cmd_start(msg: types.Message):
#     user_id = msg.from_user.id
#     user_contexts[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
#     user_resume_dicts[user_id] = {}
#
#     response = await get_gpt_reply(user_id, "")
#     await msg.answer(response)
#
#
# # Boshlash
# @dp.message_handler()
# async def handle_user_message(msg: types.Message):
#     user_id = msg.from_user.id
#
#     if user_id not in user_contexts:
#         await msg.answer("Iltimos, /start_resume buyrug‘i orqali boshlang.")
#         return
#
#     # Suhbat tarixiga foydalanuvchi javobini qo‘shamiz
#     user_contexts[user_id].append({"role": "user", "content": msg.text})
#
#     # Foydalanuvchi “ha”, “to‘g‘ri”, “tayyor” desa — fayl yaratamiz
#     if msg.text.lower() in ["ha", "to‘g‘ri", "tayyor", "boshlayver"]:
#         resume_dict = await extract_resume_dict(user_contexts[user_id])
#         filename = generate_resume_doc(resume_dict)
#         await msg.answer_document(open(filename, "rb"))
#         return
#
#     # AI'dan navbatdagi javob
#     response = await get_gpt_reply(user_id, msg.text)
#     user_contexts[user_id].append({"role": "assistant", "content": response})
#
#     # Agar AI: “json tuzaymi?” desa → dictni ko‘rsat va tasdiq so‘ra
#     if "json" in response.lower() and "yig‘ildi" in response.lower():
#         resume_dict = await extract_resume_dict(user_contexts[user_id])
#         user_resume_dicts[user_id] = resume_dict
#         await msg.answer("📄 Mana tayyor dict:\n<code>{}</code>".format(resume_dict))
#         await msg.answer("🔎 Hammasi to‘g‘rimi? Fayl yaratish uchun 'ha' deb yozing.")
#     else:
#         await msg.answer(response)
#
#     # if "json" in response.lower() and "yig‘ildi" in response.lower():
#     #     await msg.answer("♻️ JSON formatni tayyorlayman...")
#
#     #     resume_dict = await extract_resume_dict(user_contexts[user_id])
#     #     user_resume_dicts[user_id] = resume_dict
#
#     #     await msg.answer(f"<b>✅ Tayyor rezyume dict:</b>\n<code>{resume_dict}</code>")
#
#     #     # Word fayl yaratish va yuborish
#     #     filename = generate_resume_doc(resume_dict)
#     #     await msg.answer_document(open(filename, "rb"))
#
#     # else:
#     #     await msg.answer(response)
#
#
# # GPT bilan so‘zlashish
# async def get_gpt_reply(user_id, user_input):
#     messages = user_contexts[user_id]
#     chat = await openai_client.chat.completions.create(
#         model="gpt-4",
#         messages=messages,
#         temperature=0.3
#     )
#     return chat.choices[0].message.content
#
#
# # Resume dict ni so‘rab olish
# async def extract_resume_dict(messages):
#     # Faqat so‘nggi kontekstlarni yuborish
#     short_messages = messages[-15:] if len(messages) > 15 else messages
#     short_messages.append({"role": "user", "content": "Iltimos, shu suhbatdan quyidagi formatda JSON tuzib bering: "})
#
#     format_prompt = {
#         "role": "user",
#         "content": """
# Quyidagi formatda JSON tuz:
# {
#   "full_name": "...",
#   "birth_date": "...",
#   "birth_place": "...",
#   "nationality": "...",
#   "party_membership": "...",
#   "education": "...",
#   "university": "...",
#   "specialization": "...",
#   "ilmiy_daraja": "...",
#   "ilmiy_unvon": "...",
#   "languages": "...",
#   "deputat": "...",
#   "dav_mukofoti": "...",
#   "work_experience": "...",
#   "contact": "...",
#   "photo_path": "...",
#   "relatives": [
#     {
#       "relation_type": "...",
#       "full_name": "...",
#       "b_year_place": "...",
#       "job_title": "...",
#       "address": "..."
#     },
#     ...
#   ]
# }
# Faqat JSON qaytaring. Izoh yozma.
# """
#     }
#
#     full_prompt = short_messages + [format_prompt]
#
#     chat = await openai_client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=full_prompt,
#         temperature=0.3
#     )
#
#     try:
#         import json
#         return json.loads(chat.choices[0].message.content)
#     except Exception as e:
#         return {"error": f"JSON parse error: {e}"}
