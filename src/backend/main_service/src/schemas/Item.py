class Item:
    def __init__(self, 
                name: str = None):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Имя должно быть string")
        self.__name = value