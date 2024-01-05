import pytest
from api import app, db, User, Blog
import json
from flask_jwt_extended import create_access_token


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.drop_all()


def get_token(client, username, password):
    response = client.post(
        '/api/login', json={'username': username, 'password': password}
    )
    data = json.loads(response.data.decode())
    return data['access_token']


def test_register(client):
    response = client.post(
        '/api/register',
        json={'username': 'testuser', 'password': 'testpassword'},
    )
    assert response.status_code == 201
    assert json.loads(response.data.decode()) == {
        'message': 'User registered successfully'
    }


def test_login(client):
    client.post(
        '/api/register',
        json={'username': 'testuser', 'password': 'testpassword'},
    )
    response = client.post(
        '/api/login', json={'username': 'testuser', 'password': 'testpassword'}
    )
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data.decode())


def test_get_blogs(client):
    response = client.get('/api/blogs')
    assert response.status_code == 200
    assert 'blogs' in json.loads(response.data.decode())


def test_get_blog(client):
    blog = Blog(title='Test Blog', content='Test Content', author='testuser')
    db.session.add(blog)
    db.session.commit()
    response = client.get(f'/api/blogs/{blog.id}')
    assert response.status_code == 200
    assert 'blog' in json.loads(response.data.decode())


def test_create_blog(client):
    token = get_token(client, 'testuser', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post(
        '/api/blogs',
        headers=headers,
        json={'title': 'New Blog', 'content': 'New Content'},
    )
    assert response.status_code == 201
    assert json.loads(response.data.decode()) == {
        'message': 'Blog created successfully'
    }


def test_update_blog(client):
    blog = Blog(title='Test Blog', content='Test Content', author='testuser')
    db.session.add(blog)
    db.session.commit()
    token = get_token(client, 'testuser', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.put(
        f'/api/blogs/{blog.id}',
        headers=headers,
        json={'title': 'Updated Blog', 'content': 'Updated Content'},
    )
    assert response.status_code == 200
    assert json.loads(response.data.decode()) == {
        'message': 'Blog updated successfully'
    }


def test_delete_blog(client):
    blog = Blog(title='Test Blog', content='Test Content', author='testuser')
    db.session.add(blog)
    db.session.commit()
    token = get_token(client, 'testuser', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/api/blogs/{blog.id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data.decode()) == {
        'message': 'Blog deleted successfully'
    }
