from aiogram.dispatcher.filters.state import State, StatesGroup

class CategoryState(StatesGroup):
    title = State()
    desc = State()


class SubCategoryState(StatesGroup):
    title = State()
    desc = State()
    cat_id = State()