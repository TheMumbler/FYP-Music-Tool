import os
import pytest

from src.site.apps import app, db
from src.site.apps.models import User

basedir = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    app.config['DEBUG'] = False
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()
    with app.app_context():
        db.drop_all()
        db.create_all()
    # create_test_user()
    yield client


def test_home(client):
    """Test home page"""
    response = client.get('/')
    assert response.status_code == 200


def test_home_text(client):
    """Test home page"""
    response = client.get('/')
    assert response.status_code == 200


def test_tool_logged_out(client):
    """Check if user can use tool without being logged in"""
    response = client.get('/tool')
    assert response.status_code == 302


def test_login(client):
    """Test user login"""
    response = login(client, "test", "test", red=False)
    assert response.status_code == 302


def test_login_redirect(client):
    """Test user login"""
    response = login(client, "test", "test")
    assert response.status_code == 200
    response = logout(client)
    assert response.status_code == 200


def test_logout(client):
    response = login(client, "test", "test")
    assert response.status_code == 200


def test_tool_logged_in(client):
    """Check access to tool after logging in"""
    response = login(client, "test", "test")
    assert response.status_code == 200
    response = client.get('/tool', follow_redirects=True)
    assert response.status_code == 200


def test_invalid_register_dupe(client):
    """Test that duplicate accounts cannnot be made"""
    response = register(client, 'test', 'test@example.com', 'test', 'test')
    assert response.status_code == 200
    response = register(client, 'test', 'test@example.com', 'test', 'test')
    assert b'Please use a different username.' in response.data
    assert b'Please use a different email address.' in response.data


def test_invalid_email(client):
    response = register(client, 'test', 'test.com', 'test', 'test')
    assert b'Invalid email address.' in response.data


def test_valid_user_registration(client):
    """Test account registration"""
    # TODO: Fix this response data
    response = register(client, 'test', 'test@test.com', 'testing', 'testing')
    assert response.status_code == 200
    assert b'Congratulations, you are now a registered user!' in response.data


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200


def login(client, username, password, red=True):
    return client.post('/login',
                       data=dict(
                           username=username,
                           password=password),
                       follow_redirects=red)


def register(client, username, email, password, password2, redirect=True):
    return client.post('/register',
                       data=dict(username=username,
                                 email=email,
                                 password=password,
                                 password2=password2),
                       follow_redirects=redirect)


def logout(client):
    return client.get('/logout', follow_redirects=True)
