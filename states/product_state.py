from aiogram.dispatcher.filters.state import State, StatesGroup

class ProductState(StatesGroup):
    title = State()
    desc = State()
    price = State()
    sub_cat_id = State()