from aiogram import F, types, Router
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать!")