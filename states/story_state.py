from aiogram.dispatcher.filters.state import StatesGroup, State

class StoryState(StatesGroup):
    category        = State()
    sub_category = State()
    product          = State()
    amount          = State()