from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards.default import actions

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=actions)
