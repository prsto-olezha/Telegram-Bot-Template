from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(Command("starta"))
async def start(msg: Message):
    await msg.answer(f"Привет, {msg.from_user.first_name} (Админ)!")