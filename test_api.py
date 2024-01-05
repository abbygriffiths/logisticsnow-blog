import pytest
from api import app, db, Blog
import json


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
    client.post(
        '/api/register',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        },
    )
    response = client.post(
        '/api/login', json={'username': username, 'password': password}
    )
    data = json.loads(response.data.decode())
    return data['access_token']


def test_register_matching_passwords(client):
    response = client.post(
        '/api/register',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        },
    )
    assert response.status_code == 201
    assert json.loads(response.data.decode()) == {
        'message': 'User registered successfully'
    }


def test_register_non_matching_passwords(client):
    response = client.post(
        '/api/register',
        json={
            'username': 'testuser',
            'password': 'test1',
            'confirm_password': 'test2',
        },
    )
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Passwords do not match'}


def test_login_correct_password(client):
    client.post(
        '/api/register',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        },
    )
    response = client.post(
        '/api/login', json={'username': 'testuser', 'password': 'testpassword'}
    )
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data.decode())


def test_login_incorrect_password(client):
    client.post(
        '/api/register',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        },
    )
    response = client.post(
        '/api/login', json={'username': 'testuser', 'password': 'wrong'}
    )
    assert response.status_code == 401
    assert response.get_json() == {'message': 'Invalid credentials'}


def test_get_blogs(client):
    response = client.get('/api/blogs')
    assert response.status_code == 200
    assert 'blogs' in json.loads(response.data.decode())


def test_get_blog(client):
    with app.app_context():
        blog = Blog(
            title='Test Blog', content='Test Content', author='testuser'
        )
        db.session.add(blog)
        db.session.commit()
        response = client.get(f'/api/blogs/{blog.id}')
        assert response.status_code == 200
        assert 'blog' in json.loads(response.data.decode())


def test_create_blog(client):
    with app.app_context():
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
    with app.app_context():
        blog = Blog(
            title='Test Blog', content='Test Content', author='testuser'
        )
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
    with app.app_context():
        blog = Blog(
            title='Test Blog', content='Test Content', author='testuser'
        )
        db.session.add(blog)
        db.session.commit()
        token = get_token(client, 'testuser', 'testpassword')
        headers = {'Authorization': f'Bearer {token}'}
        response = client.delete(f'/api/blogs/{blog.id}', headers=headers)
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == {
            'message': 'Blog deleted successfully'
        }
