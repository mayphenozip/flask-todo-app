import sqlite3

# 1. Подключение к базе данных (файл создастся автоматически)
conn = sqlite3.connect('students.db')

# Создаем курсор для выполнения SQL-запросов
cursor = conn.cursor()

print("--- Этап 1: Создание таблицы ---")
# 2. Создание таблицы студентов
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    major TEXT
)
''')
conn.commit()
print("Таблица 'students' успешно создана или уже существует.\n")


print("--- Этап 2: Добавление данных (INSERT) ---")
# Очистим таблицу перед демонстрацией, чтобы данные не дублировались при перезапусках
cursor.execute("DELETE FROM students")
conn.commit()

# Добавление студентов (параметризованные запросы для защиты от SQL-инъекций)
students_to_add = [
    ('Алексей', 19, 'Информатика'),
    ('Мария', 20, 'Дизайн'),
    ('Иван', 18, 'Робототехника')
]

for student in students_to_add:
    cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", student)

conn.commit()
print("Студенты успешно добавлены в базу.\n")


print("--- Этап 3: Чтение данных (SELECT) ---")
# Получение всех строк из таблицы
cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()

for row in all_students:
    print(f"ID: {row[0]} | Имя: {row[1]} | Возраст: {row[2]} | Специальность: {row[3]}")
print()


print("--- Этап 4: Обновление данных (UPDATE) ---")
# Изменим специальность Алексею
cursor.execute("UPDATE students SET major = ? WHERE name = ?", ('Веб-разработка', 'Алексей'))
conn.commit()

# Проверим изменения конкретно для Алексея
cursor.execute("SELECT * FROM students WHERE name = ?", ('Алексей',))
print("После обновления:", cursor.fetchone(), "\n")


print("--- Этап 5: Удаление данных (DELETE) ---")
# Удалим Ивана из базы данных
cursor.execute("DELETE FROM students WHERE name = ?", ('Иван',))
conn.commit()

print("--- Итоговый список студентов в БД после всех операций ---")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | Имя: {row[1]} | Возраст: {row[2]} | Специальность: {row[3]}")

# Закрываем соединение с базой данных
conn.close()