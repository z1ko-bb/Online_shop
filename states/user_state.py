from aiogram.dispatcher.filters.state import StatesGroup, State

class UserForm(StatesGroup):
    lang = State()
    name = State()
    phone_number = State()
    location = State()
    confirm = State()