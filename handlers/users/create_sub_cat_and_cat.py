from aiogram import types
from loader import dp, db
from data.config import ADMINS
from states.suc_cat_cat_state import SubCategoryState, CategoryState
from states.product_state import ProductState
from aiogram.dispatcher import FSMContext
from keyboards.inline.sub_cat_and_cat import cats_button_for_sub_cats, sub_cats_button_for_add_product

@dp.message_handler(text="/create_cat", user_id=ADMINS, state="*")
async def create_cat(message: types.Message):
    await CategoryState.title.set()
    await message.answer(text="Katigoriya nomini kiriting  :)")

@dp.message_handler(state=CategoryState.title)
async def get_cat_title(message: types.Message, state: FSMContext):
    await state.update_data(
        {"title": message.text}
    )
    await CategoryState.desc.set()
    await message.answer("Katigoriya haqida to`liq ma`lumot kiriting!")

@dp.message_handler(state=CategoryState.desc)
async def finish_cat_create(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    desc = message.text
    
    await db.add_category(title=title, desc=desc)
    await state.finish()
    await message.answer(f"{title} nomli katigoriya saqlandi!")

@dp.message_handler(text="/create_sub_cat", user_id=ADMINS, state="*")
async def create_sub_cat(message: types.Message):
    await SubCategoryState.title.set()
    await message.answer(text="kichik bolim nomini kiriting: ")

@dp.message_handler(state=SubCategoryState.title)
async def get_sub_cat_title(message: types.Message, state: FSMContext):
    await state.update_data(
        {"title": message.text}
    )
    await SubCategoryState.desc.set()
    await message.answer(text="Kichik katigoriya haqida malumot kiriting!")

@dp.message_handler(state=SubCategoryState.desc)
async def get_sub_cat_desc(message: types.Message, state: FSMContext):
    await state.update_data(
        {"desc": message.text}
    )
    await SubCategoryState.cat_id.set()
    cats = cats_button_for_sub_cats(await db.get_all_cats())
    await message.answer("Qaysi kategoriyaga mansubligini tanlang!", reply_markup=cats)

@dp.callback_query_handler(state=SubCategoryState.cat_id)
async def get_cat_id(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    desc = data.get("desc")
    cat_id = int(call.data)

    await db.add_sub_category(title=title, desc=desc, cat_id=cat_id)
    await state.finish()
    await call.answer(text="Sub category added succesfully!")

@dp.message_handler(text="/add_product", state="*", user_id=ADMINS)
async def add_product(message: types.Message):
    await ProductState.title.set()
    await message.answer(text="Mahsulot nomini kiriting: ")

@dp.message_handler(state=ProductState.title)
async def get_product_title(message: types.Message, state: FSMContext):
    await state.update_data(
        {"title": message.text}
    )
    await ProductState.desc.set()
    await message.answer(text="Mahsulot haqida ma`lumot kiriting: ")

@dp.message_handler(state=ProductState.desc)
async def get_product_desc(message: types.Message, state: FSMContext):
    await state.update_data(
        {"desc": message.text}
    )
    await ProductState.price.set()
    await message.answer(text="Mahsulot narxini kiriting: ")

@dp.message_handler(state=ProductState.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(
        {"price": message.text}
    )
    await ProductState.sub_cat_id.set()
    sub_cats = sub_cats_button_for_add_product(await db.get_all_sub_cats())
    await message.answer(text="Bo`limlardan birini tanlang: ", reply_markup=sub_cats)

@dp.callback_query_handler(state=ProductState.sub_cat_id)
async def get_sub_cat_id(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    desc = data.get("title")
    price = int(data.get("price"))
    sub_cat_id = int(call.data)

    await db.add_product(title, desc, price, sub_cat_id)
    await state.finish()
    await call.message.delete()
    await call.answer(text="Mahsulot saqlandi!", cache_time=5)