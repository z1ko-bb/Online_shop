from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🤑Xarid qilish")
        ],
       [
            KeyboardButton(text="🔎Qidirish"),
            KeyboardButton(text="🛒Korzina")
       ],
        [
            KeyboardButton(text="❤️Yoqtirilgan"),
            KeyboardButton(text="🌫Xaridlar tarixi")
        ],
        [
            KeyboardButton(text="👤profil&sozlamalar")
        ]
    ],
    resize_keyboard=True
)