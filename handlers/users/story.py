from loader import db, dp
from aiogram import types
from keyboards.inline.sub_cat_and_cat import cats_button, sub_cats_button, products_button
from states.story_state import StoryState

@dp.message_handler(text="🤑Xarid qilish")
async def cats(message: types.Message):
    cats = cats_button(await db.get_all_cats())
    await StoryState.category.set()
    await message.answer(text="Keling, siz uchun birgalikda periferiya yig'amiz ✌️", reply_markup=cats)

@dp.callback_query_handler(state=StoryState.category)
async def sub_cats(call: types.CallbackQuery):
    sub_cats = sub_cats_button(await db.get_sub_cats_by_cat_id(int(call.data)))
    await StoryState.sub_category.set()
    await call.message.answer(text="Bo`limlardan birini tanglang!", reply_markup=sub_cats)

@dp.callback_query_handler(state=StoryState.sub_category)
async def products(call: types.CallbackQuery):
    product_buttons = products_button(await db.get_products_by_sub_cat_id(int(call.data)))
    await call.message.answer("Mahsulotlardan birini tanlang!", reply_markup=product_buttons)

 