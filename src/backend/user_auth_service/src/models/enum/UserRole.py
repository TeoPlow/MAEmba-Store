import enum

class UserRoleEnum(enum.Enum):
    NotVerifyed = "Not_Verifyed"
    Verifyed = "Verifyed"
    Admin = "Admin"

    @classmethod
    def list(cls):
        """Получить список всех значений Enum."""
        return [role.value for role in cls]

    def __str__(self):
        return self.value