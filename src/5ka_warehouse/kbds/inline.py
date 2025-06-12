from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def get_admin_kb(product_id: int) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Изменить", callback_data=f"update_{product_id}"))
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_{product_id}"))
    keyboard.adjust(2)
    return keyboard