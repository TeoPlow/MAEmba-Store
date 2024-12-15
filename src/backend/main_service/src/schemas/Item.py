from typing import Dict, Any


class Item:
    def __init__(self, 
                name: str = None,
                price: float = None,
                stock: int = None,
                item_category_id: int = None):
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__item_category_id = item_category_id

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Имя должно быть string")
        self.__name = value

    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Цена должна быть числом больше или равным 0")
        self.__price = value

    @property
    def stock(self) -> int:
        return self.__stock
    
    @stock.setter
    def stock(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Количество на складе должно быть целым числом больше или равным 0")
        self.__stock = value

    @property
    def item_category_id(self) -> int:
        return self.__item_category_id
    
    @item_category_id.setter
    def item_category_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID категории товара должно быть положительным целым числом")
        self.__item_category_id = value
    
    @classmethod
    def validate_data(cls, data: Dict[str, Any]) -> "Item":
        """
        Проверяет, соответствует ли словарь data требованиям класса.
        Создаёт объект, если всё верно, или вызывает исключение.
            Параметры:
                Словарь с данными для валидации.
                
            Возвращает:
                Объект Item.
        """
        try:
            return cls(
                name=data.get("name"),
                price=data.get("price"),
                stock=data.get("stock"),
                item_category_id=data.get("item_category_id")
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Ошибка валидации данных: {e}")
    
    def print_item(self) -> str:
        return (
            f"Название: {self.name}\n"
            f"Цена: {self.price}\n"
            f"Количество на складе: {self.stock}\n"
            f"ID категории товара: {self.item_category_id}"
        )
