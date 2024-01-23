from aiogram import Router
from controllers.category_contoller import CategoryCallbackFactory
from controllers.sub_classes import CreatingNote, NoteCallbackFactory
from create_bot import bot
from aiogram import F, types
from DTO.note_dto import NotePostDto
from database.note_repository import NoteRepositoryOrm
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from DTO.note_dto import NoteDto

router = Router()

now_id = -1
now_name = ""

# Вывод сообщения с клавиатурой по созданию новой записи
def keyboard_menu(main_builder: InlineKeyboardBuilder = None):
    builder = main_builder
    symbol_trash = "🗑"
    symbol_back = "⬅️"
    if builder is None:
        builder = InlineKeyboardBuilder()
    create_btn = types.InlineKeyboardButton(text="Создать запись", callback_data="create_note")
    builder.row(create_btn)
    back_btn = types.InlineKeyboardButton(text=symbol_back, callback_data="categories")
    delete_btn = types.InlineKeyboardButton(text=symbol_trash, callback_data=f"deletecategoryid_{now_id}")
    builder.row(back_btn,delete_btn )
    return builder

# Создание списка записей в виде кнопок(для далнейшего взаимодействия)
def creating_buttons_for_all_notes(notes: list[NoteDto]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for note in notes:
        id = note.id
        desc = note.description
        completed = note.completed
        symbol_completed = " ❌"
        if completed:
            symbol_completed = " ✅"
        builder.button(text=desc + symbol_completed, callback_data=f"opennoteid_{id}")
    builder.adjust(1)
    return builder

# Вывод всех записей конретной категории
async def display_all_notes(chat_id: int):
    all_notes = NoteRepositoryOrm.get_notes_by_category_id(now_id)
    str_result = f"Категория <b>{now_name}</b>\n\n--Список записей--"
    builder = None
    if not all_notes:
        str_result += "\n\n--пусто--\n\n"
    else:
        builder = creating_buttons_for_all_notes(all_notes)
    builder = keyboard_menu(builder)
    await bot.send_message(chat_id, str_result, reply_markup=builder.as_markup(), parse_mode="HTML")

# Создание кнопок меню для управления одной записью
async def create_buttons_for_one_note(note: NoteDto, chat_id: int):
    id = note.id
    desc = note.description
    completed = note.completed
    cat_id = note.category_id
    symbol_completed = "❌"
    if completed:
        symbol_completed = "✅"
    symbol_trash = "🗑"
    symbol_back = "⬅️"
    builder = InlineKeyboardBuilder()
    builder.button(text=symbol_back, callback_data=CategoryCallbackFactory(id=cat_id, name=now_name))
    builder.button(text=symbol_completed, callback_data=NoteCallbackFactory(id=id, job="switch", completed=not completed))
    builder.button(text=symbol_trash, callback_data=NoteCallbackFactory(id=id,  job="delete", completed=completed))
    builder.adjust(2)
    await bot.send_message(chat_id, desc, reply_markup=builder.as_markup())
    
# Вывод одной записи
async def display_note(chat_id: int, note_id: int):
    note = NoteRepositoryOrm.get_note_by_id(note_id)
    if not note:
        return
    await create_buttons_for_one_note(note, chat_id)

# Открытие записи по id
@router.callback_query(F.data.startswith("opennoteid_"))
async def callbacks_notes_for_note(callback: types.CallbackQuery):
    note_id = callback.data.split("_")[1]
    chat_id = callback.message.chat.id
    await callback.message.delete()
    await display_note(chat_id, note_id)

# Откытие всех записей принадлежащих опр. категории
@router.callback_query(CategoryCallbackFactory.filter())
async def callbacks_notes_for_note(callback: types.CallbackQuery, callback_data: CategoryCallbackFactory):
    category_id = callback_data.id
    name = callback_data.name
    global now_id, now_name
    now_name = name
    now_id = category_id
    chat_id = callback.message.chat.id
    await callback.message.delete()
    await display_all_notes(chat_id)
    
# Открытие записи по id
@router.callback_query(NoteCallbackFactory.filter(F.job == "delete"))
async def callbacks_notes_for_note(callback: types.CallbackQuery, callback_data: NoteCallbackFactory):
    note_id = callback_data.id
    chat_id = callback.message.chat.id
    NoteRepositoryOrm.delete_note(note_id)
    await callback.message.delete()
    await display_all_notes(chat_id)
    
# Смена состояния записи (выполнено/не выполнено)
@router.callback_query(NoteCallbackFactory.filter(F.job == "switch"))
async def callbacks_notes_for_switch_complete_note(callback: types.CallbackQuery, callback_data: NoteCallbackFactory):
    completed = callback_data.completed
    note_id = callback_data.id
    NoteRepositoryOrm.update_completed_note(note_id, completed)
    chat_id = callback.message.chat.id
    await callback.message.delete()
    await display_note(chat_id, note_id)

# Создание новой записи шаг 1 - инициализация ввода записи
@router.callback_query(F.data == "create_note")
async def callbacks_created_note_step_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreatingNote.choosing_desc)
    await bot.send_message(callback.message.chat.id, "Ожидается ввод записи...")

# Создание новой записи шаг 2 - создание записи
@router.message(CreatingNote.choosing_desc)
async def created_note_step_2(message: types.Message, state: FSMContext):
    description = message.text
    new_category = NotePostDto(description=description, category_id=now_id)
    NoteRepositoryOrm.insert_note(new_category)
    await bot.send_message(message.chat.id, f"Создана запись")
    await state.clear()
    await display_all_notes(message.chat.id)