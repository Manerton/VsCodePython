from aiogram import Router
from mytypes.note import Note
from create_bot import bot
from aiogram import F, types
from aiogram.filters import Command
from database.note_repository import get_all_notes, insert_note, update_note, update_completed_note, get_note_by_id, delete_note
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

router = Router()

now_id = -1

class NoteCallbackFactory(CallbackData, prefix="note"):
    id: int
    category_id: int
    completed: bool 
    job: str

class CreatingNote(StatesGroup):
    choosing_desc = State()

# Вывод сообщения с клавиатурой по созданию новой записи
def keyboard_menu(main_builder: InlineKeyboardBuilder = None):
    builder = main_builder
    if builder is None:
        builder = InlineKeyboardBuilder()
    create_note_btn = types.InlineKeyboardButton(text="Создать запись", callback_data="create_note")
    delete_category_btn = types.InlineKeyboardButton(text="Удалить категорию", callback_data=f"deletecategoryid_{now_id}")
    builder.row(create_note_btn)
    builder.row(delete_category_btn)
    return builder

# Создание списка записей в виде кнопок(для далнейшего взаимодействия )
def creating_buttons_for_all_notes(notes: tuple) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for note in notes:
        id = note[0]
        desc = note[1] 
        completed = note[2]
        symbol_completed = " ❌"
        if completed:
            symbol_completed = " ✅"
        builder.button(text=desc + symbol_completed, callback_data=f"opennoteid_{id}")
    builder.adjust(1)
    return builder

async def display_all_notes(chat_id: int, category_id: int):
    all_notes = get_all_notes(category_id)
    str_result = "Список записей"
    builder = None
    if not all_notes:
        str_result += "\n\n--пусто--\n\n"
    else:
        builder = creating_buttons_for_all_notes(all_notes)
    builder = keyboard_menu(builder)
    await bot.send_message(chat_id, str_result, reply_markup=builder.as_markup())

async def create_buttons_for_one_note(note, chat_id: int):
    id = note[0]
    desc = note[1]
    completed = note[2]
    cat_id = note[3]
    symbol_completed = "❌"
    if completed:
        symbol_completed = "✅"
    symbol_trash = "🗑"
    symbol_back = "⬅️"    
    builder = InlineKeyboardBuilder()
    builder.button(text=symbol_back, callback_data=f"categoryid_{cat_id}")
    builder.button(text=symbol_completed, callback_data=NoteCallbackFactory(id=id, category_id=cat_id, job="switch", completed=not completed))
    builder.button(text=symbol_trash, callback_data=NoteCallbackFactory(id=id, category_id=cat_id, job="delete", completed=completed))
    builder.adjust(2)
    await bot.send_message(chat_id, desc, reply_markup=builder.as_markup())
    

async def display_note(chat_id: int, note_id: int):
    note = get_note_by_id(note_id)
    if not note:
        return
    await create_buttons_for_one_note(note[0], chat_id)
    

# Открытие записи по id
@router.callback_query(F.data.startswith("opennoteid_"))
async def callbacks_notes_for_note(callback: types.CallbackQuery):
    note_id = callback.data.split("_")[1]
    chat_id = callback.message.chat.id
    await callback.message.delete()
    await display_note(chat_id, note_id)

# Откытие всех записей принадлежащих опр. категории
@router.callback_query(F.data.startswith("categoryid_"))
async def callbacks_notes_for_note(callback: types.CallbackQuery):
    category_id = callback.data.split("_")[1]
    global now_id
    now_id = category_id
    chat_id = callback.message.chat.id
    await callback.message.delete()
    await display_all_notes(chat_id, category_id)
    
# Открытие записи по id
@router.callback_query(NoteCallbackFactory.filter(F.job == "delete"))
async def callbacks_notes_for_note(callback: types.CallbackQuery, callback_data: NoteCallbackFactory):
    category_id = callback_data.category_id
    note_id = callback_data.id
    chat_id = callback.message.chat.id
    delete_note(note_id)
    await callback.message.delete()
    await display_all_notes(chat_id, category_id)
    
@router.callback_query(NoteCallbackFactory.filter(F.job == "switch"))
async def callbacks_notes_for_switch_complete_note(callback: types.CallbackQuery, callback_data: NoteCallbackFactory):
    category_id = callback_data.category_id
    completed = callback_data.completed
    note_id = callback_data.id
    update_completed_note(note_id, completed)
    chat_id = callback.message.chat.id
    await callback.message.delete()
    await display_note(chat_id, note_id)
    
@router.callback_query(F.data == "create_note")
async def callbacks_notes_for_category(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreatingNote.choosing_desc)
    await bot.send_message(callback.message.chat.id, "Ожидается ввод заметки...")
    
@router.message(CreatingNote.choosing_desc)
async def set_name(message: types.Message, state: FSMContext):
    description = message.text
    new_category = Note(now_id, description)
    insert_note(new_category)
    await bot.send_message(message.chat.id, f"Создана заметка")
    await state.clear()
    await display_all_notes(message.chat.id, now_id)