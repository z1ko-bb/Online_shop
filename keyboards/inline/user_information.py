from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data="uzb")
        ],
        [
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="ru")
        ],
        [
            InlineKeyboardButton(text="English 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="eng")
        ]
    ]
)