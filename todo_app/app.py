from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)
FILE_NAME = 'tasks.json'

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    new_task_text = request.form['task']
    if new_task_text:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        task_data = {
            'text': new_task_text,
            'date': current_date
        }
        tasks.append(task_data)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

@app.route('/clear_all')
def clear_all():
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

# --- ПР4: Маршрут для редактирования задачи ---
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Проверка на существование индекса задачи (из методички)
    if task_id < 0 or task_id >= len(tasks): [cite: 333]
        return "Задача не найдена", 404 [cite: 335]
    
    task = tasks[task_id]
    old_text = task['text'] # Запоминаем старый текст для самостоятельного задания 

    if request.method == 'POST': [cite: 337]
        new_text = request.form.get('task', '').strip() [cite: 339]
        
        # 1. Проверка на пустое поле (из методички)
        if new_text == '': [cite: 398]
            return render_template('edit.html', task=task, message="Текст не может быть пустым!") [cite: 399]
        
        # 2. ЗАДАНИЕ ДЛЯ САМОСТОЯТЕЛЬНОГО РЕШЕНИЯ: проверка на отсутствие изменений
        if new_text == old_text: [cite: 408]
            return render_template('edit.html', task=task, message="Ничего не изменено") [cite: 408]
        
        # Если проверки пройдены, обновляем текст (из методички)
        tasks[task_id]['text'] = new_text [cite: 345]
        save_tasks(tasks) [cite: 349]
        return redirect('/') [cite: 351]
    
    else: [cite: 353]
        return render_template('edit.html', task=task) [cite: 355]

if __name__ == '__main__':
    app.run(debug=True)