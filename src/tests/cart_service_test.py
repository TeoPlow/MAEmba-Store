import pytest
import httpx
from uuid import uuid4

BASE_URL = "http://0.0.0:8002"  # Замените на ваш URL

@pytest.fixture
def test_user_id():
    return str(uuid4())  # Генерируем UUID для тестов

@pytest.fixture
def test_cart_item():
    return {
        "item_id": 15,
        "quantity": 1
    }

@pytest.fixture
def test_cart_data():
    return {
        "items": [
            {
                "id": "225b2d01-328a-4128-8878-d5728ec93a80",
                "user_id": "eaf0673f-19b1-42ff-b07f-af22fc5172fc",
                "item_id": 15,
                "quantity": 1,
                "price": 119.9,
                "time": "2024-12-18T00:59:41.683367+03:00"
            },
            {
                "id": "abde150a-da80-43d5-ac71-9af33c6b5463",
                "user_id": "eaf0673f-19b1-42ff-b07f-af22fc5172fc",
                "item_id": 21,
                "quantity": 9,
                "price": 1079.1,
                "time": "2024-12-18T01:00:47.236604+03:00"
            }
        ]
    }

def test_get_cart_success(test_user_id, test_cart_data):
    # Тест успешного получения корзины пользователя
    response = httpx.get(f"{BASE_URL}/{test_user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "items" in data["data"]
    assert isinstance(data["data"]["items"], list)  # Проверка, что items - это список

def test_put_cart_item_success(test_user_id, test_cart_item):
    # Тест успешного добавления/обновления элемента в корзине
    response = httpx.put(f"{BASE_URL}/{test_user_id}", json=test_cart_item)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"

def test_delete_cart_item_success(test_user_id, test_cart_item):
    # Тест успешного удаления элемента из корзины
    response = httpx.delete(f"{BASE_URL}/{test_user_id}", json=test_cart_item)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"

def test_get_cart_not_found():
    # Тест, если корзина пользователя не найдена
    invalid_user_id = "00000000-0000-0000-0000-000000000000"
    response = httpx.get(f"{BASE_URL}/{invalid_user_id}")
    assert response.status_code == 404

    data = response.json()
    assert data["status"] == "error"

def test_put_cart_item_validation_error(test_user_id):
    # Тест ошибки валидации для PUT-запроса
    invalid_item = {
        "item_id": "",  # Пустой ID товара
        "quantity": -1  # Некорректное количество
    }
    response = httpx.put(f"{BASE_URL}/{test_user_id}", json=invalid_item)
    assert response.status_code == 422

    data = response.json()
    assert data["status"] == "error"
    assert "validation error" in data["message"].lower()

def test_delete_cart_item_not_found(test_user_id):
    # Тест удаления несуществующего элемента из корзины
    invalid_item = {
        "item_id": 99999  # Не существует в корзине
    }
    response = httpx.delete(f"{BASE_URL}/{test_user_id}", json=invalid_item)
    assert response.status_code == 404

    data = response.json()
    assert data["status"] == "error"
    assert "Item not found" in data["message"]
