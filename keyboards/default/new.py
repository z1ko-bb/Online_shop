from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️ share contact ", request_contact=True),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 share location ", request_location=True),
        ],
    ],
    resize_keyboard=True,
)