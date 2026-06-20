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

def sort_priority_key(task):
    priority = task.get('priority', 'средний')
    if priority == 'высокий': return 1
    elif priority == 'средний': return 2
    return 3

# Главная страница
@app.route('/')
def index():
    sorted_tasks = sorted(tasks, key=sort_priority_key)
    return render_template('index.html', tasks=sorted_tasks, filter_type='all')

@app.route('/active')
def active_tasks():
    active = [t for t in tasks if not t.get('done', False)]
    return render_template('index.html', tasks=active, filter_type='active')

@app.route('/by_priority_active')
def priority_active_tasks():
    active = [t for t in tasks if not t.get('done', False)]
    sorted_active = sorted(active, key=sort_priority_key)
    return render_template('index.html', tasks=sorted_active, filter_type='priority_active')

# --- СЛУЖЕБНЫЙ МАРШРУТ ДЛЯ СОРТИРОВКИ ПО АЛФАВИТУ (Самостоятельное задание ПР7) ---
@app.route('/alphabetical')
def alphabetical_tasks():
    # Сортируем по тексту задачи без учета регистра
    sorted_abc = sorted(tasks, key=lambda t: t.get('text', '').lower())
    return render_template('index.html', tasks=sorted_abc, filter_type='alphabetical')

# --- ПР7: Маршрут для поиска задач ---
@app.route('/search')
def search_tasks():
    query = request.args.get('query', '').strip().lower()
    # Фильтруем задачи, где поисковый запрос есть в тексте
    filtered = [t for t in tasks if query in t.get('text', '').lower()]
    return render_template('index.html', tasks=filtered, filter_type='search', search_query=query)

@app.route('/add', methods=['POST'])
def add_task():
    new_task_text = request.form['task']
    task_priority = request.form.get('priority', 'средний')
    if new_task_text:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        task_data = {
            'text': new_task_text,
            'date': current_date,
            'done': False,
            'priority': task_priority
        }
        tasks.append(task_data)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    filter_type = request.args.get('filter_type', 'all')
    search_q = request.args.get('search_query', '')
    
    if filter_type == 'active':
        current_list = [t for t in tasks if not t.get('done', False)]
    elif filter_type == 'priority_active':
        current_list = sorted([t for t in tasks if not t.get('done', False)], key=sort_priority_key)
    elif filter_type == 'alphabetical':
        current_list = sorted(tasks, key=lambda t: t.get('text', '').lower())
    elif filter_type == 'search':
        current_list = [t for t in tasks if search_q in t.get('text', '').lower()]
    else:
        current_list = sorted(tasks, key=sort_priority_key)
        
    if 0 <= task_id < len(current_list):
        target_task = current_list[task_id]
        if target_task in tasks:
            tasks.remove(target_task)
            save_tasks(tasks)
            
    if filter_type == 'active': return redirect('/active')
    elif filter_type == 'priority_active': return redirect('/by_priority_active')
    elif filter_type == 'alphabetical': return redirect('/alphabetical')
    elif filter_type == 'search': return redirect(f'/search?query={search_q}')
    return redirect('/')

@app.route('/clear_all')
def clear_all():
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    filter_type = request.args.get('filter_type', 'all')
    search_q = request.args.get('search_query', '')
    
    if filter_type == 'active':
        current_list = [t for t in tasks if not t.get('done', False)]
    elif filter_type == 'priority_active':
        current_list = sorted([t for t in tasks if not t.get('done', False)], key=sort_priority_key)
    elif filter_type == 'alphabetical':
        current_list = sorted(tasks, key=lambda t: t.get('text', '').lower())
    elif filter_type == 'search':
        current_list = [t for t in tasks if search_q in t.get('text', '').lower()]
    else:
        current_list = sorted(tasks, key=sort_priority_key)

    if task_id < 0 or task_id >= len(current_list):
        return "Задача не найдена", 404
        
    target_task = current_list[task_id]
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
        tasks[actual_index]['priority'] = new_priority
        save_tasks(tasks)
        
        if filter_type == 'active': return redirect('/active')
        elif filter_type == 'priority_active': return redirect('/by_priority_active')
        elif filter_type == 'alphabetical': return redirect('/alphabetical')
        elif filter_type == 'search': return redirect(f'/search?query={search_q}')
        return redirect('/')
    else:
        return render_template('edit.html', task=task, filter_type=filter_type)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    filter_type = request.args.get('filter_type', 'all')
    search_q = request.args.get('search_query', '')
    
    if filter_type == 'active':
        current_list = [t for t in tasks if not t.get('done', False)]
    elif filter_type == 'priority_active':
        current_list = sorted([t for t in tasks if not t.get('done', False)], key=sort_priority_key)
    elif filter_type == 'alphabetical':
        current_list = sorted(tasks, key=lambda t: t.get('text', '').lower())
    elif filter_type == 'search':
        current_list = [t for t in tasks if search_q in t.get('text', '').lower()]
    else:
        current_list = sorted(tasks, key=sort_priority_key)

    if 0 <= task_id < len(current_list):
        target_task = current_list[task_id]
        actual_index = tasks.index(target_task)
        tasks[actual_index]['done'] = not tasks[actual_index].get('done', False)
        save_tasks(tasks)
        
    if filter_type == 'active': return redirect('/active')
    elif filter_type == 'priority_active': return redirect('/by_priority_active')
    elif filter_type == 'alphabetical': return redirect('/alphabetical')
    elif filter_type == 'search': return redirect(f'/search?query={search_q}')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)