import pytest
from app import app
import database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    database.init_db()
    with app.test_client() as client:
        yield client

def test_login_success(client):
    # 1. Проверяем успешный вход admin / 1234 (под твой app.py)
    response = client.post('/login', data={'username': 'admin', 'password': '1234'})
    assert response.status_code == 302
    
    with client.session_transaction() as sess:
        assert sess.get('is_admin') is True

def test_login_failure(client):
    # 2. Проверяем неверный пароль
    response = client.post('/login', data={'username': 'admin', 'password': 'wrong_password'})
    assert response.status_code == 200
    
    with client.session_transaction() as sess:
        assert sess.get('is_admin') is not True

def test_delete_without_auth(client):
    # 3. Попытка удаления без авторизации
    response = client.get('/delete/1')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_delete_with_auth(client):
    # 4. Удаление под авторизованным админом
    with client.session_transaction() as sess:
        sess['is_admin'] = True
        
    response = client.get('/delete/1')
    assert response.status_code == 302