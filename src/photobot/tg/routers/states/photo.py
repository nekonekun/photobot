from aiogram.fsm.state import State, StatesGroup


class PhotoEdit(StatesGroup):
    editing = State()
