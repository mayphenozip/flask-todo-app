import pytest
from app import app
import database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    database.init_db()
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_message_redirect(client):
    response = client.post('/add', data={
        'name': 'Tester',
        'message': 'Hello from pytest!'
    })
    assert response.status_code == 302

def test_add_message_empty(client):
    response = client.post('/add', data={
        'name': '',
        'message': ''
    })
    assert response.status_code == 302