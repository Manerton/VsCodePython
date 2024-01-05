from database.db import execute_sql_command_without_res, execute_sql_command_with_res
from mytypes.category import Category

# Возвращает все категории
def get_all_categories():
    command = f"SELECT * FROM category"
    res = execute_sql_command_with_res(command)
    return res

# Возвращает контретную категорию по id
def get_categories_by_id(categories_id: int):
    command = f"SELECT * FROM category WHERE id={categories_id}"
    res = execute_sql_command_with_res(command)
    return res

# Возвращает контретную категорию по названию
def get_categories_by_name(name: str):
    command = f"SELECT * FROM category WHERE name=\"{name}\""
    res = execute_sql_command_with_res(command)
    return res

# Добавляет категорию в таблицу
def insert_category(category: Category):
    command = f"INSERT INTO category (name) VALUES (\"{category.name}\")"
    execute_sql_command_without_res(command)
    
# Удаляет категорию из таблицы
def delete_category(category_id: int):
    command = f"DELETE FROM category WHERE id={category_id}"
    # При удалении категории нужно удалить все записи в этой категории
    execute_sql_command_without_res(command)