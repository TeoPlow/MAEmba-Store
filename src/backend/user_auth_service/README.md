# Сервис управления пользователями и аутентификацией.

Перед использованием нужно создать базу данных PostgreSQL. 

Пример:
```
psql -U postgres

CREATE DATABASE mae_store_user_auth_db;
```

Далее нужно внести данные для подключение к серверу в конфиг *.env* и запустить alembic.ini командой:
```
alembic upgrade head

# Хороший ответ:
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 63d22fa12aab, user_auth_tables
```
## **/{user_id}**

Возвращает данные пользователя или изменяет данные пользователя.
- ### GET

    Запрос:

        GET http://0.0.0.0:8001/e5f8433e-76a9-4509-87f0-e1b12354d92b
        

    Ответ:
    ```json
    {
    "status":"success",
    "data": {
        "id":"e5f8433e-76a9-4509-87f0-e1b12354d92b",
        "email":"AGUREZ@yandex.com",
        "user_type":"ind",
        "username":"egor228",
        "contact_number":"+79853553825",
        "user_role":"Not_Verifyed",
        "created":"2024-12-15T15:48:46.195517+03:00",
        "updated":"2024-12-15T21:01:34.382072+03:00"
        }
    }
    ```

- ### PUT

    Запрос:

        PUT http://0.0.0.0:8001/e5f8433e-76a9-4509-87f0-e1b12354d92b

    ```json
    { 
    "email": "AGUREZ@yandex.com",
    "user_role":"Verifyed",
    }
    ```


    Ответ:
    ```json
    {
    "status":"success"
    }
    ```

## **/register**

Регистрирует пользователя. 

Возвращает ID зарегестрированного пользователя.
- ### POST 

    Запрос:

        POST http://0.0.0.0:8001/auth/register

    ```json
    {
    "user_type": "ind", 
    "username": "egor228", 
    "password": "password", 
    "email": "citymodz@yandex.com", 
    "contact_number": "+79853553825"
    }
    ```
        

    Ответ:
    ```json
    {
    "status": "success", 
    "data": {
        "user_id": "e5f8433e-76a9-4509-87f0-e1b12354d92b"
        }
    }
    ```

## **/login**

Авторизует пользователя. 

Возвращает токен авторизации и время его работы, чтобы потом из них создать куку.
- ### POST 

    Запрос:

        POST http://0.0.0.0:8001/auth/login

    ```json
    {
    "email_or_name": "username",
    "password": "pass12345",
    "remember_me": true
    }
    ```
        

    Ответ:
    ```json
    {
    "status": "success", 
    "data": {
        "token": "eeee1234-76a9-4509-87f0-e1b12354d92b", 
        "token-expiry": 2592000.0
        }
    }
    ```

## **/send-confirmation-email**

Отправляю пользователю ссылку на почту для авторизации.
- ### POST 

    Запрос:

        POST http://0.0.0.0:8001/auth/send-confirmation-email

    ```json
    {
    "email": "kruyneg@mail.ru",
    "user_id": "eeee1234-76a9-4509-87f0-e1b12354d92b"
    }
    ```
        

    Ответ:
    ```json
    {
    "status": "success",
    "message": "Письмо отправлено, проверьте почту."
    }
    ```