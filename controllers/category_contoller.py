from mytypes.category import Category
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.category_repository import get_all_categories, get_categories_by_name, insert_category
from create_bot import bot
from controllers.note_contoller import get_all_notes

router = Router()

@router.message(Command("categories"))
async def display_all_categories(message: types.Message):
    categories = get_all_categories()
    builder = InlineKeyboardBuilder()
    if categories is None or not categories:
        await bot.send_message(message.chat.id, "Список пуст")
        return 
    for category in categories:
        id = category[0]
        name = category[1]
        btn = types.InlineKeyboardButton(text=name, callback_data=f"categoryid_{id}")
        builder.row(btn)
    await bot.send_message(message.chat.id, "Список категорий", reply_markup=builder.as_markup())
    
    


class CreatingCategory(StatesGroup):
    choosing_name = State()

@router.message(Command("create_category"))
async def create_new_category(message: types.Message, state: FSMContext):
    await state.set_state(CreatingCategory.choosing_name)
    await bot.send_message(message.chat.id, "Введите название категории!")
    
@router.message(CreatingCategory.choosing_name)
async def set_name(message: types.Message, state: FSMContext):
    name = message.text
    temp_category = get_categories_by_name(name)
    if temp_category:
        await bot.send_message(message.chat.id, f"Категория {temp_category} уже существует")
        return
    new_category = Category(name)
    insert_category(new_category)
    await bot.send_message(message.chat.id, f"Создана категория {name}")
    await state.clear()