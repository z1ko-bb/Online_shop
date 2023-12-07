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


confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="yes"),
            InlineKeyboardButton(text="❌Yo`q", callback_data="no")
        ]
    ]
)