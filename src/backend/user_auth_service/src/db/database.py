from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# База данных для пользователя
BaseUsers = declarative_base()

SQLALCHEMY_DATABASE_USERS_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine_users = create_engine(SQLALCHEMY_DATABASE_USERS_URL)
SessionLocalUsers = sessionmaker(autocommit=False, autoflush=False, bind=engine_users)

# Зависимость для получения сессии базы данных
def get_db_users():
    db = SessionLocalUsers()
    try:
        yield db
    finally:
        db.close()