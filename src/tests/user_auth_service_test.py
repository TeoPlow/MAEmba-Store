import pytest
import httpx
from uuid import UUID
BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture
def test_register_data():
    return {
        "user_type": "ind",
        "username": "abcabc",
        "password": "passsword",
        "email": "AGUREZZ@yandex.com",
        "contact_number": "+77953553825"
    }

@pytest.fixture
def test_login_data():
    return {
        "email_or_name": "eor228",
        "password": "pasword",
        "remember_me": True,
    }

@pytest.fixture
def test_user_id():
    return "eaf0673f-19b1-42ff-b07f-af22fc5172fc"


@pytest.fixture
def test_user_data():
    return {
        "user_type": "ind",
        "username": "egor228",
        "password": "password",
        "email": "AGUREZZ@yandex.com",
        "contact_number": "+79853553825"
    }


def test_register_success(test_register_data):
    #Тест успешной регистрации пользователя.
    response = httpx.post(f"{BASE_URL}/auth/register", json=test_register_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "user_id" in data["data"]
    assert UUID(data["data"]["user_id"])  # Проверяем, что user_id является UUID


def test_register_validation_error():
    #Тест ошибки валидации при регистрации.
    invalid_user_data = {
        "user_type": "ind",
        "username": "",  # Пустое имя
        "password": "password",
        "email": "not-an-email",  # Некорректный email
        "contact_number": "123",  # Некорректный номер
    }
    response = httpx.post(f"{BASE_URL}/auth/register", json=invalid_user_data)
    assert response.status_code == 422

    data = response.json()
    assert data["status"] == "error"
    assert "validation error" in data["message"].lower()


def test_login_success(test_login_data):


    # Выполним авторизацию
    response = httpx.post(f"{BASE_URL}/auth/login", json=test_login_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "token" in data["data"]
    assert UUID(data["data"]["token"])  # Проверяем, что token является UUID
    assert "token-expiry" in data["data"]


def test_login_invalid_credentials(test_login_data):
    #Тест ошибки авторизации с неверными данными.
    invalid_login_data = {
        "email_or_name": "wrong_username",
        "password": "wrong_password",
        "remember_me": True,
    }
    response = httpx.post(f"{BASE_URL}/auth/login", json=invalid_login_data)
    assert response.status_code == 401

    data = response.json()
    assert data["status"] == "error"
    assert "Invalid credentials" in data["message"]


def test_get_user_success(test_user_id):
    #Тест успешного выполнения GET-запроса.
    response = httpx.get(f"{BASE_URL}/{test_user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["id"] == test_user_id
    assert data["data"]["email"] == "AGUREZ@yandex.com"
    assert data["data"]["user_type"] == "ind"
    assert data["data"]["username"] == "egor228"
    assert data["data"]["contact_number"] == "+79853553825"
    assert data["data"]["user_role"] == "Not_Verifyed"
    assert "created" in data["data"]
    assert "updated" in data["data"]


def test_get_user_not_found():
    #Тест для случая, если пользователь не найден.
    invalid_user_id = "00000000-0000-0000-0000-000000000000"
    response = httpx.get(f"{BASE_URL}/{invalid_user_id}")
    assert response.status_code == 404

    data = response.json()
    assert data["status"] == "error"
    assert "User not found" in data["message"]


def test_put_user_success(test_user_id, test_user_data):
    #Тест успешного выполнения PUT-запроса.
    response = httpx.put(f"{BASE_URL}/{test_user_id}", json=test_user_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"


def test_put_user_validation_error(test_user_id):
    #Тест ошибки валидации для PUT-запроса.
    invalid_data = {
        "user_type": "ind",
        "username": "",  # Пустое имя
        "password": "password",
        "email": "not-an-email",  # Некорректный email
        "contact_number": "123"  # Некорректный номер
    }
    response = httpx.put(f"{BASE_URL}/{test_user_id}", json=invalid_data)
    assert response.status_code == 404

    data = response.json()
    assert data["status"] == "error"
    assert "validation error" in data["message"].lower()
