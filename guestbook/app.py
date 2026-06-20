from flask import Flask, render_template, request, redirect
from datetime import datetime
import database

app = Flask(__name__)

# Функция для красивого форматирования даты по-русски (Задание Д)
def format_russian_date(date_str):
    try:
        # Парсим стандартную дату из БД
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля", 
            5: "мая", 6: "июня", 7: "июля", 8: "августа", 
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        return f"{dt.day} {months[dt.month]} {dt.year} г. в {dt.strftime('%H:%M')}"
    except:
        return date_str # Если что-то пошло не так, вернем оригинал

@app.route('/')
def index():
    raw_messages = database.get_all_messages()
    
    # Преобразуем сообщения, делая дату красивой (Задание Д)
    messages = []
    for msg in raw_messages:
        msg_dict = dict(msg)
        msg_dict['created_at'] = format_russian_date(msg_dict['created_at'])
        messages.append(msg_dict)
        
    # Забираем ошибку и старые значения, если они были переданы из /add
    error = request.args.get('error')
    old_name = request.args.get('old_name', '')
    old_message = request.args.get('old_message', '')
    
    return render_template('index.html', messages=messages, error=error, old_name=old_name, old_message=old_message)

@app.route('/add', methods=['POST'])
def add_msg():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    # Задание Г: Валидация на пустые поля
    if not name or not message:
        # Если хотя бы одно поле пустое, возвращаем пользователя на главную и передаем параметры ошибки
        return redirect(f"/?error=1&old_name={name}&old_message={message}")
        
    # Сохраняем дату в стабильном формате ISO для сортировки (Задание Д)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    database.add_message(name, message, current_time)
        
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)