import sqlite3

DATABASE = 'guestbook.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ВОТ ЭТА ФУНКЦИЯ ДОЛЖНА БЫТЬ ТУТ:
def init_db():
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

# Функции из ПР11 (убедись, что они тоже на месте)
def delete_message(message_id):
    with get_db() as conn:
        conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
        conn.commit()

def get_message_count():
    with get_db() as conn:
        cursor = conn.execute('SELECT COUNT(*) FROM messages')
        return cursor.fetchone()[0]

def clear_all_messages():
    with get_db() as conn:
        conn.execute('DELETE FROM messages')
        conn.commit()