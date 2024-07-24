from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import src.FSM as FSM

router = Router()

@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await msg.answer(f"Привет, {msg.from_user.first_name}!")
    await state.set_state(FSM.FSMFill.MENU)