# Сервис корзины покупок.

## **/{user_id}**

Возвращает, изменяет, удаляет содержимое корзины по ID пользователя.
- ### GET

    Запрос:

        GET http://0.0.0.0:8002/e5f8433e-76a9-4509-87f0-e1b12354d92b
        

    Ответ:
    ```json
    {
    "status":"success",
    "data": {
        "items": [
                {
                "id": "225b2d01-328a-4128-8878-d5728ec93a80", 
                "user_id": "e5f8433e-76a9-4509-87f0-e1b12354d92b", 
                "item_id": 15, 
                "quantity": 1, 
                "price": 119.9, 
                "time": "2024-12-18T00:59:41.683367+03:00"
                }, 
                {
                "id": "abde150a-da80-43d5-ac71-9af33c6b5463", 
                "user_id": "e5f8433e-76a9-4509-87f0-e1b12354d92b", 
                "item_id": 21, 
                "quantity": 9, 
                "price": 1079.1, 
                "time": "2024-12-18T01:00:47.236604+03:00"
                }
            ]
        }
    }
    ```

- ### PUT

    Запрос:

        PUT http://0.0.0.0:8002/e5f8433e-76a9-4509-87f0-e1b12354d92b

    ```json
    {
    "item_id": 15, 
    "quantity": 1 
    }
    ```


    Ответ:
    ```json
    {
    "status":"success"
    }
    ```

- ### DELETE

    Запрос:

        DELETE http://0.0.0.0:8002/e5f8433e-76a9-4509-87f0-e1b12354d92b

    ```json
    {
    "item_id": 15
    }
    ```


    Ответ:
    ```json
    {
    "status":"success"
    }
    ```