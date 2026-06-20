import sqlite3

DATABASE = 'guestbook.db'

def get_db():
    # Функция открывает соединение с БД и настраивает выдачу результатов в виде словарей
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Создание таблицы по ТЗ из методички
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

def get_all_messages():
    # Задание из ПР9: Новые сообщения должны появляться сверху (сортируем по id DESC)
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM messages ORDER BY id DESC')
        return cursor.fetchall()

def add_message(name, message, created_at):
    with get_db() as conn:
        conn.execute(
            'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
            (name, message, created_at)
        )
        conn.commit()