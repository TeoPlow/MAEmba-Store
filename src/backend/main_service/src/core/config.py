import os
from dotenv import load_dotenv

load_dotenv()

USER_API_URL = os.getenv("USER_API_URL")
MODEL_API_URL = os.getenv("MODEL_API_URL")
ITEMS_API_URL = os.getenv("ITEMS_API_URL")
CART_API_URL = os.getenv("CART_API_URL")
ORDER_API_URL = os.getenv("ORDER_API_URL")

LOG_LEVEL = os.getenv("LOG_LEVEL")
