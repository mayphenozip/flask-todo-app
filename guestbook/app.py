from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import database

app = Flask(__name__)

database.init_db()

def format_russian_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля", 
            5: "мая", 6: "июня", 7: "июля", 8: "августа", 
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        return f"{dt.day} {months[dt.month]} {dt.year} г. в {dt.strftime('%H:%M')}"
    except:
        return date_str

@app.route('/')
def index():
    raw_messages = database.get_all_messages()
    
    messages = []
    for msg in raw_messages:
        msg_dict = dict(msg)
        msg_dict['created_at'] = format_russian_date(msg_dict['created_at'])
        messages.append(msg_dict)
        
    error = request.args.get('error')
    old_name = request.args.get('old_name', '')
    old_message = request.args.get('old_message', '')
    
    # Задание 5: Получаем актуальное количество сообщений
    count = database.get_message_count()
    
    return render_template('index.html', messages=messages, error=error, old_name=old_name, old_message=old_message, count=count)

@app.route('/add', methods=['POST'])
def add_msg():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    if not name or not message:
        return redirect(f"/?error=1&old_name={name}&old_message={message}")
        
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    database.add_message(name, message, current_time)
    return redirect('/')

# --- ПР11: Маршрут для удаления одного сообщения ---
@app.route('/delete/<int:message_id>')
def delete_msg(message_id):
    database.delete_message(message_id)
    return redirect('/')

# --- Самостоятельное задание Е: Страница-предупреждение об удалении всего ---
@app.route('/delete-all-confirm')
def delete_all_confirm_page():
    return render_template('delete_confirm.html')

# --- Самостоятельное задание Е: Маршрут полного удаления ---
@app.route('/clear_all_messages', methods=['POST'])
def clear_all():
    database.clear_all_messages()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)