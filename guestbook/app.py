from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import database

app = Flask(__name__)

# Секретный ключ, чтобы Flask мог шифровать сессии куки (cookie)
app.secret_key = 'very-secret-key-1234'

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
    count = database.get_message_count()
    
    # Передаем в шаблон статус: админ перед нами или нет
    is_admin = session.get('is_admin', False)
    
    return render_template('index.html', messages=messages, error=error, old_name=old_name, old_message=old_message, count=count, is_admin=is_admin)

@app.route('/add', methods=['POST'])
def add_msg():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    if not name or not message:
        return redirect(f"/?error=1&old_name={name}&old_message={message}")
        
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    database.add_message(name, message, current_time)
    return redirect('/')

# --- ПР12: Страница входа в админку ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Проверяем учетные данные по заданию
        if username == 'admin' and password == '1234':
            session['is_admin'] = True  # Запоминаем админа в сессии
            return redirect('/')
        else:
            login_error = "Неверный логин или пароль!"
            
    return render_template('login.html', login_error=login_error)

# --- Самостоятельное задание Ж: Выход из сессии админа ---
@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect('/')

# --- ПР12: Защищенное удаление одного сообщения ---
@app.route('/delete/<int:message_id>')
def delete_msg(message_id):
    if not session.get('is_admin', False):
        return redirect('/login')  # Выкидываем на логин, если пытается удалить не админ
        
    database.delete_message(message_id)
    return redirect('/')

# --- ПР12: Защищенная страница подтверждения очистки базы ---
@app.route('/delete-all-confirm')
def delete_all_confirm_page():
    if not session.get('is_admin', False):
        return redirect('/login')
    return render_template('delete_confirm.html')

# --- ПР12: Защищенный сброс всех сообщений ---
@app.route('/clear_all_messages', methods=['POST'])
def clear_all():
    if not session.get('is_admin', False):
        return redirect('/login')
        
    database.clear_all_messages()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)