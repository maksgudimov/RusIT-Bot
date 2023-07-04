from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class ScriptsInsert(StatesGroup):
    name = State()
    description = State()
    price = State()
    img = State()

class ScriptLeafThrough(StatesGroup):
    throuhgt = State()

class Form(StatesGroup):
    name = State()
    phone = State()

class Cooperation(StatesGroup):
    what = State()
    other = State()
    answer = State()
    phone = State()

class Refactor(StatesGroup):
    refactor = State()
    choose = State()
    name = State()
    description = State()
    price = State()
    img = State()

class AdminAllMess(StatesGroup):
    messAll = State()

class AdminOneMess(StatesGroup):
    call = State()
    messOne = State()

class AdminInsertProjects(StatesGroup):
    name = State()
    img = State()


class CollabWithUser(StatesGroup):
    doc = State()

class AdminJokes(StatesGroup):
    name = State()
    joke = State()

class ChatGPT(StatesGroup):
    mess = State()