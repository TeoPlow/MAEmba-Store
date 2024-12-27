import streamlit as st
import requests
from uuid import UUID

BASE_URL = "http://0.0.0.0:8000"  # URL вашего FastAPI-приложения

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
        response = requests.get(f"{BASE_URL}/{user_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

def update_user_info():
    st.header("Обновление информации о пользователе")
    user_id = st.text_input("Введите UUID пользователя", "")
    email = st.text_input("Email")
    user_role = st.text_input("Роль пользователя")
    if st.button("Обновить информацию"):
        if not validate_uuid(user_id):
            st.error("Некорректный UUID")
            return
        data = {"email": email, "user_role": user_role}
        response = requests.put(f"{BASE_URL}/user/{user_id}", json=data)
        if response.status_code == 200:
            st.success("Информация о пользователе обновлена!")
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

def register_user():
    st.header("Регистрация пользователя")
    user_type = st.selectbox("Тип пользователя", ["ind", "org"])
    username = st.text_input("Имя пользователя")
    password = st.text_input("Пароль", type="password")
    email = st.text_input("Email")
    contact_number = st.text_input("Номер телефона")
    if st.button("Зарегистрироваться"):
        data = {
            "user_type": user_type,
            "username": username,
            "password": password,
            "email": email,
            "contact_number": contact_number
        }
        response = requests.post(f"{BASE_URL}/user/auth/register", json=data)
        if response.status_code == 200:
            data_to_email = {"email": data["email"], "user_id": response.json()["data"]["user_id"]}
            response_to_email = requests.post(f"{BASE_URL}/user/auth/send-confirmation-email", json=data_to_email)
            if response_to_email.status_code == 200:
                st.success("Пользователь успешно зарегистрирован! Авторизуйте вашу почту по сслыке, которая оптравлена на вашу почту")
                st.json(response_to_email.json())
            else:
                st.error(f"Ошибка: {response_to_email.status_code} - {response_to_email.text}")
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

def login_user():
    st.header("Авторизация пользователя")
    email_or_name = st.text_input("Email или имя пользователя")
    password = st.text_input("Пароль", type="password")
    remember_me = st.checkbox("Запомнить меня")
    if st.button("Войти"):
        data = {
            "email_or_name": email_or_name,
            "password": password,
            "remember_me": remember_me
        }
        response = requests.post(f"{BASE_URL}/user/auth/login", json=data)
        if response.status_code == 200:
            st.success("Успешный вход!")
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

def logout_user():
    st.header("Выход пользователя")
    user_id = st.text_input("Введите UUID пользователя", "")
    if st.button("Выйти"):
        if not validate_uuid(user_id):
            st.error("Некорректный UUID")
            return
        data = {"user_id": user_id}
        response = requests.post(f"{BASE_URL}/user/auth/logout", json=data)
        if response.status_code == 200:
            st.success("Пользователь успешно вышел из системы!")
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

def send_confirmation_email():
    st.header("Отправка подтверждающего письма")
    email = st.text_input("Email")
    user_id = st.text_input("UUID пользователя")
    if st.button("Отправить письмо"):
        if not validate_uuid(user_id):
            st.error("Некорректный UUID")
            return
        data = {"email": email, "user_id": user_id}
        response = requests.post(f"{BASE_URL}/user/auth/send-confirmation-email", json=data)
        if response.status_code == 200:
            st.success("Письмо успешно отправлено!")
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

def confirm_email():
    st.header("Подтверждение почты")
    token = st.text_input("Введите токен")
    if st.button("Подтвердить почту"):
        response = requests.get(f"{BASE_URL}/user/auth/confirm-email/{token}")
        if response.status_code == 200:
            st.success("Почта успешно подтверждена!")
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

def validate_auth():
    st.header("Проверка аутентификации")
    auth_token = st.text_input("Введите токен авторизации")
    if st.button("Проверить"):
        data = {"auth_token": auth_token}
        response = requests.post(f"{BASE_URL}/user/auth/validate-auth", json=data)
        if response.status_code == 200:
            st.success("Аутентификация подтверждена!")
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")
# Навигация
st.title("MAEMBA Store API Frontend")
st.sidebar.title("Меню")
option = st.sidebar.selectbox("Выберите действие", [
    "Информация о пользователе",
    "Обновление информации о пользователе",
    "Регистрация пользователя",
    "Авторизация пользователя",
    "Выход пользователя",
    "Отправка подтверждающего письма",
    "Подтверждение почты",
    "Проверка аутентификации",
])

if option == "Информация о пользователе":
    get_user_info()
elif option == "Обновление информации о пользователе":
    update_user_info()
elif option == "Регистрация пользователя":
    register_user()
elif option == "Авторизация пользователя":
    login_user()
elif option == "Выход пользователя":
    logout_user()
elif option == "Подтверждение почты":
    confirm_email()
elif option == "Проверка аутентификации":
    validate_auth()

elif option == "Рекомендует цену":
    recomendation()
