from aiogram import types
import logging
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate
from loader import dp, bot
from data.config import CHANNELS
from keyboards.inline.subscription import check_button
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    channels_format = str()
    channel_kb = ReplyKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        logging.info(invite_link)
        # channel_kb.insert(KeyboardButton(text=f"{chat.title}", url=))
        channels_format += f"➡️ <a href='{invite_link}'><b>{chat.title}</b></a>\n"

    await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n\n"
                         f"{channels_format}",
                         reply_markup=check_button,
                         disable_web_page_preview=True,
                         parse_mode="HTML")