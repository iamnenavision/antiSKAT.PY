
import os.path
import sqlite3
from typing import List


def create_table() -> None:
    """Создаёт таблицу, если ее нет(нет файла data.db)"""
    check_file = os.path.exists("data.db")
    if check_file:  # файл существует, просто выходим
        return
    db = sqlite3.connect("data.db", check_same_thread=False)
    cur = db.cursor()
    cur.execute("""CREATE TABLE user_info (
        id text,
        first_name text,
        last_name text,
    )""")
    db.commit()
    db.close()


def find_in_db(_id: str) -> bool:
    """Ищем по id в базе данных, true - если user есть в базе данных"""
    db = sqlite3.connect("data.db", check_same_thread=False)
    cur = db.cursor()
    user = cur.execute(
        f"SELECT * FROM user_info WHERE id = '{_id}'").fetchall()
    db.close()
    return user != []


def print_info_db() -> None:
    """Выводит всех пользователей в терминал"""
    db = sqlite3.connect("data.db", check_same_thread=False)
    cur = db.cursor()
    info = cur.execute("SELECT * FROM user_info").fetchall()
    for user in info:
        print(*user)
    db.close()


def insert_user_db(_id: str, first_name: str, last_name: str) -> None:
    """Добавление пользователя в базу данных"""
    db = sqlite3.connect("data.db", check_same_thread=False)
    cur = db.cursor()
    cur.execute(
        f"INSERT INTO user_info VALUES('{_id}', '{first_name}', '{last_name}')")
    db.commit()
    db.close()


def get_user_info_db(_id: str) -> List[str]:
    """Возвращает информацию о пользователе [id, first_name, last_name]"""
    db = sqlite3.connect("data.db", check_same_thread=False)
    cur = db.cursor()
    info = cur.execute(
        f"SELECT * FROM user_info WHERE id = '{_id}'").fetchone()
    db.close()
    return info


def update_user_info_db(_id: str, first_name: str, last_name: str) -> None:
    """Обновление данных пользователя"""
    db = sqlite3.connect("data.db", check_same_thread=False)
    cur = db.cursor()
    cur.execute(
        f"UPDATE user_info SET first_name = '{first_name}', last_name = '{last_name}' WHERE id = '{_id}'")
    db.commit()
    db.close()


if __name__ == "__main__":
    # проверка на сущестование базы данных
    create_table()
    print_info_db()