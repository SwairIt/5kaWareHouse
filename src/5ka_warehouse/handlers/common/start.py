from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# from sqlite3 import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product, orm_update_product, orm_get_products, orm_get_product

from kbds.inline import get_admin_kb


router = Router()


@router.message(StateFilter(None), CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать!")


@router.message(StateFilter(None), Command("all_products"))
async def all_products_cmd(message: types.Message, session: AsyncSession):
    products = await orm_get_products(session)

    for product in products:
        await message.answer(f"Название: {product.name}\nЦена: {product.price}\nКол-во: {product.quantity}\nАртикул: {product.article}", reply_markup=get_admin_kb(product.id).as_markup())
    await message.answer("Все товары 🔝")


############ FSM ################################

class AddProduct(StatesGroup):
    name = State()
    price = State()
    quantity = State()
    category = State()

    product_for_change = None


@router.message(StateFilter(None), Command("new_product"))
async def new_product(message: types.Message, session: AsyncSession, state: FSMContext):
    AddProduct.product_for_change = await orm_get_product(session, 4)

    await message.answer("Введите название товара")
    await state.set_state(AddProduct.name)


@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    await state.clear()
    await message.answer("Действия отменены")


@router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        await state.update_data(name=message.text)
    
    await message.answer("Введите цену товара")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.name)
async def add_name2(message: types.Message):
    await message.answer("Введите текст!")


@router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(price=AddProduct.product_for_change.price)
    elif message.text.isdigit():
        await state.update_data(price=message.text)
    else:
        await message.answer("Введите число!")
        return
    
    await message.answer("Введите кол-во")
    await state.set_state(AddProduct.quantity)


@router.message(AddProduct.price)
async def add_price2(message: types.Message):
    await message.answer("Введите число!")


@router.message(AddProduct.quantity, F.text)
async def add_quantity(message: types.Message, state: FSMContext):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(quantity=AddProduct.product_for_change.quantity)
    elif message.text.isdigit():
        await state.update_data(quantity=message.text)
    else:
        await message.answer("Введите число!")
        return
    
    await message.answer("Введите id категории(потом будут inline кнопки!!!)")
    await state.set_state(AddProduct.category)


@router.message(AddProduct.quantity)
async def add_quantity2(message: types.Message):
    await message.answer("Введите число!")


@router.message(AddProduct.category, F.text)
async def add_category(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(category_id=AddProduct.product_for_change.category)
    elif message.text.isdigit():
        await state.update_data(category_id=message.text)
    else:
        await message.answer("Введите число!")
        return
    
    data = await state.get_data()

    try:
        if AddProduct.product_for_change:
            await orm_update_product(session, AddProduct.product_for_change.id, data)
        else:
            await orm_add_product(session, data)
        await message.answer("Товар добавлен/изменен")
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру",)
        await state.clear()


@router.message(AddProduct.category)
async def add_quantity2(message: types.Message):
    await message.answer("Введите число!")
