from flask import Flask, render_template, request, redirect
from datetime import datetime
import database

app = Flask(__name__)

# Инициализируем базу данных при старте приложения
database.init_db()

@app.route('/')
def index():
    # Получаем все сообщения из БД (они уже отсортированы «новые сверху»)
    messages = database.get_all_messages()
    return render_template('index.html', messages=messages)

# Задел на ПР10 (Маршрут добавления, чтобы приложение уже было интерактивным)
@app.route('/add', methods=['POST'])
def add_msg():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    if name and message:
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        database.add_message(name, message, current_time)
        
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)