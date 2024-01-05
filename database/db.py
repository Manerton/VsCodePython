import sqlite3
from config import DATABASE_NAME

def execute_sql_command_with_res(command: str) -> list:
    connect = sqlite3.connect(DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    connect.commit()
    cursor.close()
    connect.close()
    return result

def execute_sql_command_without_res(command: str):
    connect = sqlite3.connect(DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute(command)
    connect.commit()
    cursor.close()
    connect.close()

def create_main_tables():
    connect = sqlite3.connect(DATABASE_NAME)
    cursor = connect.cursor()
    
    command = "CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(50))"
    cursor.execute(command)
    
    command = '''CREATE TABLE IF NOT EXISTS note 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    description varchar(50),
    id_category int, 
    FOREIGN KEY (id_category) REFERENCES CLIENTS (id))'''
    cursor.execute(command)
    
    connect.commit()
    cursor.close()
    connect.close()