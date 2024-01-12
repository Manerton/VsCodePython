from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup

class CategoryCallbackFactory(CallbackData, prefix="category"):
    id: int
    name: str

class CreatingCategory(StatesGroup):
    choosing_name = State()

class DeletingCategory(StatesGroup):
    confirm_selection = State()

class NoteCallbackFactory(CallbackData, prefix="note"):
    id: int
    completed: bool 
    job: str

class CreatingNote(StatesGroup):
    choosing_desc = State()