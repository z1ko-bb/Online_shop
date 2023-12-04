from loader import dp, bot
from aiogram import types
from states.user_state import UserForm
from aiogram.dispatcher import FSMContext
from keyboards.default.new import phone_number, location

@dp.callback_query_handler(text="uzb", state=UserForm.lang)
async def set_lang(call: types.CallbackQuery, state: FSMContext):
    lang = call.message.text
    print(lang)
    await state.update_data(
        {"lang": lang}
    )
    await call.message.delete()
    await call.message.answer(text="✍️ Ismingizni kiriting:")
    await UserForm.name.set()

@dp.message_handler(state=UserForm.name)
async def get_user_name(message: types.Message, state: FSMContext):
    name = message.text
    print(name)
    await state.update_data(
        {"name": name}
    )

    await message.answer(text="✍️ Telefon raqamingizni kiriting:\n(+998XXxxxXxXx)", reply_markup=phone_number)
    await UserForm.location.set()

@dp.message_handler(state=UserForm.location)
async def get_user_phone(message: types.Message, state:FSMContext):
    phone = message.text
    print(phone)
    await state.update_data(
        {"phone_number": phone}
    )

    await message.answer(text="📍 Lokatsiyangizni jonating!", reply_markup=location)
    await UserForm.confirm.set()