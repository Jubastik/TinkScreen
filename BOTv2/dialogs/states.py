from aiogram.fsm.state import StatesGroup, State


class MenuSG(StatesGroup):
    main = State()


class CheckSG(StatesGroup):
    main = State()
    info = State()


class HistorySG(StatesGroup):
    main = State()
    info = State()
