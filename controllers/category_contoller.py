from controllers.sub_classes import CategoryCallbackFactory, CreatingCategory, DeletingCategory
from mytypes.category import Category
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.category_repository import get_all_categories, get_categories_by_name, insert_category, delete_category
from create_bot import bot
from controllers.note_contoller import get_all_notes, delete_note

router = Router()

@router.callback_query(F.data == "categories")
async def callback_categories(callback: types.CallbackQuery):
    await display_all_categories(callback.message)

async def display_all_categories(message: types.Message):
    categories = get_all_categories()
    builder = InlineKeyboardBuilder()
    if categories is None or not categories:
        await bot.send_message(message.chat.id, "Список пуст")
        return 
    builder = creating_buttons_for_all_categories(categories)
    builder = category_keyboard_menu(builder)
    await bot.send_message(message.chat.id, "Список категорий", reply_markup=builder.as_markup())
    
# Создание кнопок для всех категорий для дальнейшего взаимодействия
def creating_buttons_for_all_categories(categories: tuple):
    builder = InlineKeyboardBuilder()
    for category in categories:
        id = category[0]
        name = category[1]
        builder.button(text=name, callback_data=CategoryCallbackFactory(id=id, name=name))
    builder.adjust(1)
    return builder

# Вывод сообщения с клавиатурой по созданию новой категории
def category_keyboard_menu(main_builder: InlineKeyboardBuilder = None):
    builder = main_builder
    if builder is None:
        builder = InlineKeyboardBuilder()
    create_category_btn = types.InlineKeyboardButton(text="Создать категорию", callback_data="create_category")
    builder.row(create_category_btn)
    return builder

# Создание новой категории шаг 1 - Ввод названия категории
@router.callback_query(F.data == "create_category")
async def callbacks_create_new_category(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreatingCategory.choosing_name)
    await bot.send_message(callback.message.chat.id, "Введите название категории!")

# Создание новой категории шаг 2 - Создание категории 
@router.message(CreatingCategory.choosing_name)
async def set_name(message: types.Message, state: FSMContext):
    name = message.text
    temp_category = get_categories_by_name(name)
    if temp_category:
        await bot.send_message(message.chat.id, f"Категория {temp_category[1]} уже существует")
        return
    new_category = Category(name)
    insert_category(new_category)
    await bot.send_message(message.chat.id, f"Создана категория {name}")
    await state.clear()
    await display_all_categories(message)
    
delete_category_id = -1
    
# Удаление категории шаг 1 - повторное потверждение от пользователя
@router.callback_query(F.data.startswith("deletecategoryid_"))
async def callbacks_delete_category_step_1(callback: types.CallbackQuery, state: FSMContext):
    global delete_category_id
    delete_category_id = callback.data.split("_")[1]
    await state.set_state(DeletingCategory.confirm_selection)
    await bot.send_message(callback.message.chat.id, "Вы уверены (Y/N):")

# Удаление категории шаг 1 - Удаление категории со всеми записями
@router.message(DeletingCategory.confirm_selection)
async def delete_category_step_2(message: types.Message, state: FSMContext):
    message_text = message.text
    if str.lower(message_text) != 'y':
        await bot.send_message(message.chat.id, f"Удаление отменено")
    else:
        all_notes = get_all_notes(delete_category_id)
        for note in all_notes:
            id = note[0]
            delete_note(id)
        delete_category(delete_category_id)
        await bot.send_message(message.chat.id, f"Категория удалена")
    await state.clear()
    await display_all_categories(message)    