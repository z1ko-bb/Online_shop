import re
from loader import dp, bot, db
from aiogram import types
from states.user_state import UserForm
from aiogram.dispatcher import FSMContext
from keyboards.default.new import phone_number, location
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.user_information import confirm
from keyboards.inline.user_information import lang

@dp.callback_query_handler(text="uzb", state=UserForm.lang)
async def set_lang(call: types.CallbackQuery, state: FSMContext):
    lang = call.data
    await state.update_data(
        {"lang": lang}
    )
    await call.message.delete()
    await call.message.answer(text="✍️ Ismingizni kiriting:")
    await UserForm.name.set()

@dp.message_handler(state=UserForm.name)
async def get_user_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {"name": name}
    )

    await message.answer(text="✍️ Telefon raqamingizni kiriting:\n(998XXxxxXxXx)", reply_markup=phone_number)
    await UserForm.location.set()

@dp.message_handler(content_types=['contact', 'text'], state=UserForm.location)
async def get_user_phone(message: types.Message, state:FSMContext):
    andoza = "(?:[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"
    try:
        phone = message.contact.phone_number
    except:
        phone = message.text
    if re.match(andoza, phone):
        await state.update_data(
            {"phone_number": phone}
        )

        await message.answer(text="📍 Lokatsiyangizni jonating!", reply_markup=location)
        await UserForm.confirm.set()
    else:
        await UserForm.location.set()
        await message.answer(text="Faqat o`zbek nomeri kiriting yoki raqamni qayta tekshiring (998977902815)")

@dp.message_handler(content_types=['location'], state=UserForm.confirm)
async def confirm_info(message: types.Message, state: FSMContext):
    lngtude = message.location.longitude
    lttude = message.location.latitude
    location = [lngtude, lttude]
    await state.update_data(
        {"location": location}
    )

    data = await state.get_data()
    confirm_txt = f"Sizning ma`lumotlaringiz!\n\n🚩Til:            {data.get('lang')}\n👨‍🦰Ism:          {data.get('name')}\n📞 Aloqa:     {data.get('phone_number')}\n\nAgar ma`lumotlar to`gri bo`lsa ularni tasdiqlang!"
    await message.answer(text=confirm_txt, reply_markup=confirm)

@dp.callback_query_handler(text="no", state="*")
async def last(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await UserForm.lang.set()
    await call.answer()
    msg = f"Salom xush kelibsiz\n👤 <b>{call.from_user.full_name}</b>!\nTilni tanlang: 🔽" 
    await call.message.answer(msg, reply_markup=lang)

@dp.callback_query_handler(text="yes", state="*")
async def confirm_yes(call: types.CallbackQuery, state: FSMContext):
    tg_id = call["from"]["id"]
    data = await state.get_data()
    name = data.get("name")
    lang = data.get("lang")
    phone_number = data.get("phone_number")
    location = data.get("location")
    location_lat = str(location[0])
    location_long = str(location[1])
    confirm = "yes"

    await db.update_user_info_for_confirm(name, lang, phone_number, location_lat, location_long, confirm, telegram_id=tg_id)
    await call.message.answer(text=".", reply_markup=ReplyKeyboardRemove())