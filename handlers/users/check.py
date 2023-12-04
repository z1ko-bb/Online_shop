from loader import dp, bot
from data.config import CHANNELS
from utils.misc import subscription
from aiogram import types
from keyboards.inline.user_information import lang
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from states.user_state import UserForm
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await UserForm.lang.set()
    await call.answer()
    final_status = True
    channel_bt = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        chat = await bot.get_chat(channel)
        if status:
            final_status *= status
            invite_link = await chat.export_invite_link()
            channel_bt.insert(InlineKeyboardButton(text=f"✅ {chat.title}", url=invite_link))

        else:
            final_status *= False
            invite_link = await chat.export_invite_link()
            channel_bt.insert(InlineKeyboardButton(text=f"❌ {chat.title}", url=invite_link))


    if final_status:
        await call.message.delete()
        msg = f"Salom xush kelibsiz\n👤 <b>{call.from_user.full_name}</b>!\nTilni tanlang: 🔽" 
        await call.message.answer(msg, reply_markup=lang)
    else:
        await call.message.delete()
        channel_bt.insert(InlineKeyboardButton(text="✔️ Obunani tekshirish", callback_data="check_subs"))
        await call.message.answer(text="Barcha knallarga obuna bolishingiz shart!", disable_web_page_preview=True, reply_markup=channel_bt)