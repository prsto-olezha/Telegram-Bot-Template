from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage 

storage = RedisStorage.from_url("redis://user:password@127.0.0.1:6379/0")
class FSMFill(StatesGroup):
    MENU = State()