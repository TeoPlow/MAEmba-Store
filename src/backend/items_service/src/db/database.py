from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# Базовый класс для моделей
BaseItems = declarative_base()

# URL для подключения к базе данных
SQLALCHEMY_DATABASE_ITEMS_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine_items = create_engine(SQLALCHEMY_DATABASE_ITEMS_URL)

# Создание сессии
SessionLocalItems = sessionmaker(autocommit=False, autoflush=False, bind=engine_items)

# Зависимость для получения сессии базы данных
def get_db_items():
    db = SessionLocalItems()
    try:
        yield db
    finally:
        db.close()