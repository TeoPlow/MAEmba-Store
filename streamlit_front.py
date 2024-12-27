import streamlit as st
import requests
from uuid import UUID

BASE_URL = "http://localhost:8000"  # URL вашего FastAPI-приложения


# Проверка на валидность UUID
def validate_uuid(uuid_string):
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False


# Функции для каждого эндпоинта
def get_user_info():
    st.header("Получение информации о пользователе")
    user_id = st.text_input("Введите UUID пользователя", "")
    if st.button("Получить информацию"):
        if not validate_uuid(user_id):
            st.error("Некорректный UUID")
            return
        response = requests.get(f"{BASE_URL}/user/{user_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")


def register_user():
    st.header("Регистрация пользователя")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    if st.button("Зарегистрироваться"):
        data = {"email": email, "password": password}
        response = requests.post(f"{BASE_URL}/user/auth/register", json=data)
        if response.status_code == 200:
            st.success("Пользователь успешно зарегистрирован!")
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")


def login_user():
    st.header("Авторизация пользователя")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        data = {"email": email, "password": password}
        response = requests.post(f"{BASE_URL}/user/auth/login", json=data)
        if response.status_code == 200:
            st.success("Успешный вход!")
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")


def create_order():
    st.header("Создание заказа")
    user_id = st.text_input("ID пользователя")
    items = st.text_area("Список товаров (в формате JSON)")
    if st.button("Создать заказ"):
        try:
            data = {"user_id": user_id, "items": eval(items)}
            response = requests.post(f"{BASE_URL}/order/create", json=data)
            if response.status_code == 200:
                st.success("Заказ успешно создан!")
                st.json(response.json())
            else:
                st.error(f"Ошибка: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Ошибка: {e}")


def get_order_info():
    st.header("Получение информации о заказе")
    order_id = st.text_input("Введите ID заказа")
    if st.button("Получить информацию о заказе"):
        if not validate_uuid(order_id):
            st.error("Некорректный UUID")
            return
        response = requests.get(f"{BASE_URL}/order/{order_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")


def get_all_orders():
    st.header("Получение всех заказов")
    user_id = st.text_input("Введите ID пользователя")
    if st.button("Получить заказы"):
        response = requests.get(f"{BASE_URL}/order/all",
                                params={"user_id": user_id})
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")


# Навигация
st.title("MAEMBA Store API Frontend")
st.sidebar.title("Меню")
option = st.sidebar.selectbox("Выберите действие", [
    "Информация о пользователе",
    "Регистрация пользователя",
    "Авторизация пользователя",
    "Создание заказа",
    "Информация о заказе",
    "Получение всех заказов",
])

if option == "Информация о пользователе":
    get_user_info()
elif option == "Регистрация пользователя":
    register_user()
elif option == "Авторизация пользователя":
    login_user()
elif option == "Создание заказа":
    create_order()
elif option == "Информация о заказе":
    get_order_info()
elif option == "Получение всех заказов":
    get_all_orders()
