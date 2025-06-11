from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product, orm_update_product

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать!")


############ FSM ################################

class AddProduct(StatesGroup):
    name = State()
    price = State()
    quantity = State()
    category = State()

    product_for_change = None


@router.message(StateFilter(None), Command("new_product"))
async def new_product(message: types.Message, state: FSMContext):
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


@router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        await state.update_data(price=message.text)
    
    await message.answer("Введите кол-во")
    await state.set_state(AddProduct.quantity)


@router.message(AddProduct.quantity, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(quantity=AddProduct.product_for_change.quantity)
    else:
        await state.update_data(quantity=message.text)
    
    await message.answer("Введите id категории(потом будут inline кнопки!!!)")
    await state.set_state(AddProduct.category)


@router.message(AddProduct.category, F.text)
async def add_price(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(category=AddProduct.product_for_change.category)
    else:
        await state.update_data(category=message.text)
    
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

    await message.answer("Введите id категории(потом будут inline кнопки!!!)")
    await state.set_state(AddProduct.category)



@router.message(Command("new_product"))
async def new_product(message: types.Message, session: AsyncSession):
    new_product = await orm_add_product(session,
                                        {
                                            "name": "Йогурт ФрутоНяня",
                                            "price": 59.90,
                                            "quantity": 100,
                                            "category_id": 1
                                        })
    
    await message.answer(f"Создан товар: {new_product.name}, артикул: {new_product.article}")