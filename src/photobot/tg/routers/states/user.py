from aiogram.fsm.state import State, StatesGroup


class Options(StatesGroup):
    waiting_for_language = State()
