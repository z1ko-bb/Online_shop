from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate
from loader import dp, bot, db
from data.config import CHANNELS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(IsPrivate(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    try:
        await db.add_user(full_name=message['from']['first_name'], telegram_id=message['from']['id'], username=message['from']['username'])
        channel_kb = InlineKeyboardMarkup(row_width=1)
        for channel in CHANNELS:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            channel_kb.insert(InlineKeyboardButton(text=f"➡️ {chat.title}\n", url=invite_link))
        channel_kb.insert(InlineKeyboardButton(text="✔️ Obunani tekshirish", callback_data="check_subs"))

        await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n\n",
                            reply_markup=channel_kb,
                            disable_web_page_preview=True,
                            parse_mode="HTML")
    except:
        channel_kb = InlineKeyboardMarkup(row_width=1)
        for channel in CHANNELS:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            channel_kb.insert(InlineKeyboardButton(text=f"➡️ {chat.title}\n", url=invite_link))
        channel_kb.insert(InlineKeyboardButton(text="✔️ Obunani tekshirish", callback_data="check_subs"))

        await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n\n",
                            reply_markup=channel_kb,
                            disable_web_page_preview=True,
                            parse_mode="HTML")