import sqlite3
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os


class DB:
    db_path = ''
    # conn = sqlite3.connect(db_path)  # или :memory: чтобы сохранить в RAM
    # cursor = conn.cursor()

    conn = None
    cursor = None

    path = "settings.ini"

    config = configparser.ConfigParser()
    config.read(path)

    def __init__(self):

        self.db_path = 'telegram_db.db'

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        check = 0
        if os.stat(self.db_path).st_size:  # файл может создаваться с ошибками и быть просто пыстым файлом
            check = self.select('SELECT EXISTS(SELECT * FROM online)')  # Проверяем есть ли хоть что-то в таблице
        if not check:
            print('Creating DB file')
            self.refresh_db()

    def refresh_db(self):

        try:
            self.select("select 'drop table ' || name || ';' from sqlite_master where type = 'table';")  # Конструкция роняет все таблицы даже не зная из названий
        except Exception:
            self.create_db()

    def create_db(self):

        # Создание таблицы
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS online
                          (user text, date text, time text)
                       """)

        self.conn.commit()

    def select(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def insert(self, table, *args):

        data = args

        try:
            self.cursor.executemany(f"INSERT INTO {table} VALUES (?, ?, ?, ?)", (data,))
        except sqlite3.IntegrityError:
            pass
        self.conn.commit()

    def test_connection(self, table):  # Проверка соединения. Хотя применяется эта функция для инициализации init класса
        return self.select(f'SELECT EXISTS(SELECT * FROM {table})')


if __name__ == '__main__':

    pass
