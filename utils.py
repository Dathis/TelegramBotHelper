from aiogram.dispatcher.filters.state import State,StatesGroup

class States(StatesGroup):
    menu = State()
    weather = State()
    music = State()
    news = State()
    books = State()
