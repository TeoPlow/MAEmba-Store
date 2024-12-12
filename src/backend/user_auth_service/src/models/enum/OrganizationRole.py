import enum

class OrganizationRoleEnum(enum.Enum):
    NotVerifyed = "Not_Verifyed"
    Verifyed = "Verifyed"

    @classmethod
    def list(cls):
        """Получить список всех значений Enum."""
        return [role.value for role in cls]

    def __str__(self):
        return self.value