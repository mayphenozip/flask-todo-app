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

# Главная страница (показывает ВСЕ задачи)
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, filter_active=False)

# Самостоятельное задание: Маршрут для отображения только активных задач
@app.route('/active')
def active_tasks():
    # Оставляем только те задачи, у которых done == False
    active = [t for t in tasks if not t.get('done', False)]
    return render_template('index.html', tasks=active, filter_active=True)

@app.route('/add', methods=['POST'])
def add_task():
    new_task_text = request.form['task']
    if new_task_text:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        # ПР5: Добавляем поле done: False по умолчанию
        task_data = {
            'text': new_task_text,
            'date': current_date,
            'done': False
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

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404
    
    task = tasks[task_id]
    old_text = task['text']

    if request.method == 'POST':
        new_text = request.form.get('task', '').strip()
        if new_text == '':
            return render_template('edit.html', task=task, message="Текст не может быть пустым!")
        if new_text == old_text:
            return render_template('edit.html', task=task, message="Ничего не изменено")
        
        tasks[task_id]['text'] = new_text
        save_tasks(tasks)
        return redirect('/')
    else:
        return render_template('edit.html', task=task)

# --- ПР5: Маршрут переключения статуса выполнения ---
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        # Меняем статус на противоположный (True -> False, False -> True)
        tasks[task_id]['done'] = not tasks[task_id].get('done', False)
        save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)