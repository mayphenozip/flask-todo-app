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

# Вспомогательная функция для сортировки по приоритету (ПР6)
def sort_priority_key(task):
    priority = task.get('priority', 'средний')
    if priority == 'высокий':
        return 1
    elif priority == 'средний':
        return 2
    else:  # низкий
        return 3

# Главная страница (Показывает ВСЕ задачи, отсортированные по приоритету)
@app.route('/')
def index():
    # Сортируем список задач перед выводом
    sorted_tasks = sorted(tasks, key=sort_priority_key)
    return render_template('index.html', tasks=sorted_tasks, filter_type='all')

# Маршрут ПР5: Показать только активные
@app.route('/active')
def active_tasks():
    active = [t for t in tasks if not t.get('done', False)]
    return render_template('index.html', tasks=active, filter_type='active')

# Самостоятельное задание №2: Только активные задачи, ОТСОРТИРОВАННЫЕ по приоритету
@app.route('/by_priority_active')
def priority_active_tasks():
    active = [t for t in tasks if not t.get('done', False)]
    sorted_active = sorted(active, key=sort_priority_key)
    return render_template('index.html', tasks=sorted_active, filter_type='priority_active')

@app.route('/add', methods=['POST'])
def add_task():
    new_task_text = request.form['task']
    # Получаем приоритет из выпадающего списка формы (ПР6)
    task_priority = request.form.get('priority', 'средний')
    
    if new_task_text:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        task_data = {
            'text': new_task_text,
            'date': current_date,
            'done': False,
            'priority': task_priority  # Сохраняем приоритет
        }
        tasks.append(task_data)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # Внимание: из-за сортировки на главной странице индексы отображения могут отличаться от реальных. 
    # Безопаснее удалять по совпадению текста/даты или отсортированному списку.
    # Так как мы передаем loop.index0 от отсортированного списка, определим какую задачу удаляем:
    filter_type = request.args.get('filter_type', 'all')
    
    if filter_type == 'active':
        current_list = [t for t in tasks if not t.get('done', False)]
    elif filter_type == 'priority_active':
        current_list = sorted([t for t in tasks if not t.get('done', False)], key=sort_priority_key)
    else:
        current_list = sorted(tasks, key=sort_priority_key)
        
    if 0 <= task_id < len(current_list):
        target_task = current_list[task_id]
        if target_task in tasks:
            tasks.remove(target_task)
            save_tasks(tasks)
            
    # Возвращаем пользователя туда, откуда он удалил
    if filter_type == 'active':
        return redirect('/active')
    elif filter_type == 'priority_active':
        return redirect('/by_priority_active')
    return redirect('/')

@app.route('/clear_all')
def clear_all():
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Применяем аналогичную логику поиска задачи из-за сортировки на главной
    filter_type = request.args.get('filter_type', 'all')
    if filter_type == 'active':
        current_list = [t for t in tasks if not t.get('done', False)]
    elif filter_type == 'priority_active':
        current_list = sorted([t for t in tasks if not t.get('done', False)], key=sort_priority_key)
    else:
        current_list = sorted(tasks, key=sort_priority_key)

    if task_id < 0 or task_id >= len(current_list):
        return "Задача не найдена", 404
        
    target_task = current_list[task_id]
    # Находим индекс этой задачи в основном глобальном списке задач
    actual_index = tasks.index(target_task)
    
    task = tasks[actual_index]
    old_text = task['text']
    old_priority = task.get('priority', 'средний')

    if request.method == 'POST':
        new_text = request.form.get('task', '').strip()
        new_priority = request.form.get('priority', 'средний')
        
        if new_text == '':
            return render_template('edit.html', task=task, message="Текст не может быть пустым!", filter_type=filter_type)
        if new_text == old_text and new_priority == old_priority:
            return render_template('edit.html', task=task, message="Ничего не изменено", filter_type=filter_type)
        
        tasks[actual_index]['text'] = new_text
        tasks[actual_index]['priority'] = new_priority  # Обновляем приоритет при редактировании
        save_tasks(tasks)
        
        if filter_type == 'active':
            return redirect('/active')
        elif filter_type == 'priority_active':
            return redirect('/by_priority_active')
        return redirect('/')
    else:
        return render_template('edit.html', task=task, filter_type=filter_type)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    filter_type = request.args.get('filter_type', 'all')
    if filter_type == 'active':
        current_list = [t for t in tasks if not t.get('done', False)]
    elif filter_type == 'priority_active':
        current_list = sorted([t for t in tasks if not t.get('done', False)], key=sort_priority_key)
    else:
        current_list = sorted(tasks, key=sort_priority_key)

    if 0 <= task_id < len(current_list):
        target_task = current_list[task_id]
        actual_index = tasks.index(target_task)
        tasks[actual_index]['done'] = not tasks[actual_index].get('done', False)
        save_tasks(tasks)
        
    if filter_type == 'active':
        return redirect('/active')
    elif filter_type == 'priority_active':
        return redirect('/by_priority_active')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)