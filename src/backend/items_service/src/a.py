import os
from alembic.config import Config
from alembic.command import upgrade, revision

# Путь к конфигурации Alembic
alembic_config = Config("alembic.ini")

# revision(alembic_config, "Созданы таблицы items и categories", autogenerate=True)

# Применение миграций
upgrade(alembic_config, "head")
