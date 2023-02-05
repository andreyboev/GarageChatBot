from aiogram.fsm.state import StatesGroup, State


class CitiesGameState(StatesGroup):
    start = State()
    city = State()
    finish = State()