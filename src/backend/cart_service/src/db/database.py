from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.logging import log

from src.core.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# База данных для пользователя
BaseCart = declarative_base()

SQLALCHEMY_DATABASE_CART_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine_cart = create_engine(SQLALCHEMY_DATABASE_CART_URL)
SessionLocalCart = sessionmaker(autocommit=False, autoflush=False, bind=engine_cart)

# Зависимость для получения сессии базы данных
def get_db_cart():
    db = SessionLocalCart()
    try:
        log.debug("Совершаю запрос к БД")
        yield db
    finally:
        db.close()