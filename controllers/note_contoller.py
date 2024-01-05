from aiogram import Router
from mytypes.note import Note
from create_bot import bot
from aiogram import F, types
from aiogram.filters import Command
from database.note_repository import get_all_notes, insert_note
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

now_id = -1

class CreatingNote(StatesGroup):
    choosing_desc = State()

# Вывод сообщения с клавиатурой по созданию новой записи
async def keyboard_menu(message: types.Message, str_res: str, main_builder: InlineKeyboardBuilder = None):
    builder = main_builder
    if builder is None:
        builder = InlineKeyboardBuilder()
    create_note_btn = types.InlineKeyboardButton(text="Создать запись", callback_data="create_note")
    builder.row(create_note_btn)
    await bot.send_message(message.chat.id, str_res, reply_markup=builder.as_markup())

# Создание списка записей в виде кнопок(для далнейшего взаимодействия )
def creating_buttons_for_all_notes(notes: tuple) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for note in notes:
        id = note[0]
        desc = note[1]
        cat_id = note[2]
        create_note_btn = types.InlineKeyboardButton(text=desc, callback_data=f"noteid_{id}")
        builder.row(create_note_btn)
    return builder

async def display_all_notes(message: types.Message, category_id: int):
    all_notes = get_all_notes(category_id)
    str_result = "Список Записей"
    builder = None
    if not all_notes:
        str_result += "\n\n--пусто--\n\n"
    else:
        builder=creating_buttons_for_all_notes(all_notes)
    await keyboard_menu(message, str_result, builder)

@router.callback_query(F.data.startswith("categoryid_"))
async def callbacks_notes_for_category(callback: types.CallbackQuery):
    category_id = callback.data.split("_")[1]
    global now_id
    now_id = category_id
    await display_all_notes(callback.message, category_id)
    
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
    await display_all_notes(message, now_id)