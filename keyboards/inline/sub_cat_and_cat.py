from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def cats_button(db_cats):
    cats = InlineKeyboardMarkup(row_width=2)
    for cat in db_cats:
        cats.insert(InlineKeyboardButton(text=cat["title"], callback_data=cat["id"]))
    
    cats.add(InlineKeyboardButton(text="⬅️Orqaga", callback_data="back"), InlineKeyboardButton(text="🏠Bosh sahifa", callback_data="home"))

    return cats

def cats_button_for_sub_cats(db_cats):
    cats = InlineKeyboardMarkup(row_width=2)
    for cat in db_cats:
        cats.insert(InlineKeyboardButton(text=cat["title"], callback_data=cat["id"]))
    
    return cats

def sub_cats_button(db_sub_cats):
    sub_cats = InlineKeyboardMarkup(row_width=2)
    for sub_cat in db_sub_cats:
        sub_cats.insert(InlineKeyboardButton(text=sub_cat["title"], callback_data=sub_cat["id"]))

    sub_cats.add(InlineKeyboardButton(text="⬅️Orqaga", callback_data="back"), InlineKeyboardButton(text="🏠Bosh sahifa", callback_data="home"))

    return sub_cats

def sub_cats_button_for_add_product(db_sub_cats):
    sub_cats = InlineKeyboardMarkup(row_width=2)
    for sub_cat in db_sub_cats:
        sub_cats.insert(InlineKeyboardButton(text=sub_cat["title"], callback_data=sub_cat["id"]))

    return sub_cats

def products_button(db_products):
    products = InlineKeyboardMarkup(row_width=2)
    for product in db_products:
        products.insert(InlineKeyboardButton(text=product["title"], callback_data=product["id"]))

    products.add(InlineKeyboardButton(text="⬅️Orqaga", callback_data="back"), InlineKeyboardButton(text="🏠Bosh sahifa", callback_data="home"))

    return products