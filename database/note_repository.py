from database.db import execute_sql_command_without_res, execute_sql_command_with_res
from mytypes.note import Note

# Возвращает все записи по конкретной категории
def get_all_notes(category_id: int): 
    command = f"SELECT * FROM note WHERE id_category={category_id}"
    res = execute_sql_command_with_res(command)
    return res

# Возвращает контретную запись по id
def get_note_by_id(note_id: int):
    command = f"SELECT * FROM note WHERE id={note_id}"
    res = execute_sql_command_with_res(command)
    return res

# Добавление записи в таблицу
def insert_note(note: Note):
    command = f"INSERT INTO note (description, completed, id_category) VALUES (\"{note.description}\",{note.completed},{note.id_category})"
    execute_sql_command_without_res(command)

# Обновление записи в таблице
def update_note(note: Note, note_id: int):
    
    command =   f"""
                    UPDATE note 
                    SET description = \"{note.description}\",
                        completed = {note.completed}
                    WHERE id = {note_id}
                """
    execute_sql_command_without_res(command)
    
# Обновление статус в таблице 
def update_completed_note(note_id: int, completed: bool):
    command =   f"UPDATE note SET completed={completed} WHERE id = {note_id}"
    execute_sql_command_without_res(command)

# Удаление записи из таблицы
def delete_note(note_id: int):
    command = f"DELETE FROM note WHERE id={note_id}"
    execute_sql_command_without_res(command)