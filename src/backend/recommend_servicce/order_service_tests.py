import pytest
import httpx
from uuid import uuid4

BASE_URL = "http://localhost:8080"  # Замените на ваш URL

@pytest.fixture
def test_user_id():
    return "eaf0673f-19b1-42ff-b07f-af22fc5172fc"

@pytest.fixture
def test_order_data():
    return {
        "order_id": "70fde51b-13d8-4398-8df6-55a2413cc544",
        "user_id": "eaf0673f-19b1-42ff-b07f-af22fc5172fc",
        "items": [
            {"item_id": 15, "quantity": 1, "price": 119.9},
            {"item_id": 21, "quantity": 9, "price": 1079.1}
        ],
        "status": "pending",
        "created_at": "2024-12-18T00:59:41.683367+03:00"
    }

@pytest.fixture
def test_order_update():
    return {
        "order_id": "70fde51b-13d8-4398-8df6-55a2413cc544",
        "status": "CANCELLED"
    }

def test_ping_pong():
    # Тест проверки доступности сервиса
    response = httpx.get(f"{BASE_URL}/ping")
    assert response.status_code == 200
    assert response.text == '"pong"'

def test_get_user_orders_success(test_user_id):
    # Тест успешного получения всех заказов пользователя
    response = httpx.get(f"{BASE_URL}/user={test_user_id}")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    
    # Проверка первого заказа в списке
    first_order = data[0]
    assert "order_id" in first_order
    assert "status" in first_order

def test_get_order_by_id_success(test_order_data):
    # Тест успешного получения информации о заказе
    order_id = test_order_data["order_id"]
    response = httpx.get(f"{BASE_URL}/order={order_id}")
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["order_id"] == order_id

def test_get_order_not_found():
    # Тест, если заказ не найден
    invalid_order_id = "00000000-0000-0000-0000-000000000000"
    response = httpx.get(f"{BASE_URL}/order={invalid_order_id}")
    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data

def test_put_update_status_success(test_order_update):
    # Тест успешного обновления статуса заказа
    response = httpx.put(f"{BASE_URL}/update-status", json=test_order_update)
    assert response.status_code == 422
    data = response.json()
    assert data['status'] == 'success'

def test_put_update_status_validation_error():
    # Тест ошибки валидации при обновлении статуса заказа
    invalid_update = {"order_id": "", "status": ""}
    response = httpx.put(f"{BASE_URL}/update-status", json=invalid_update)
    assert response.status_code == 422
    data = response.json()
    assert 'detail' in data

def test_post_create_order_success(test_order_data):
    # Тест успешного добавления нового заказа
    response = httpx.post(f"{BASE_URL}/", json=test_order_data)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'


def test_post_create_order_validation_error():
    # Тест ошибки валидации при создании заказа
    invalid_order = {
        "user_id": "invalid-uuid",
        "items": [{"item_id": "", "quantity": -1}],
        "status": "pending"
    }
    response = httpx.post(f"{BASE_URL}/", json=invalid_order)
    assert response.status_code == 422
    data = response.json()
    assert 'detail' in data
