from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    native_language = State()
    goal = State()
    english_level = State()
    topic = State()

