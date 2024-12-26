from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from src.models import Item, Category, Semicategory

class ItemHandler:

    async def get_category_by_id(self, db: Session, _id: int):
        try:
            category = (
                db.query(Category)
                .options(joinedload(Category.semicategories))  # Загружаем подкатегории
                .filter(Category.id == _id)
                .first()
            )

            if category:
                self.logger.info(f"(Get category by ID) Found category with ID {_id}")
            else:
                self.logger.info(f"(Get category by ID) No category found with ID {_id}")

            return category
        except Exception as e:
            self.logger.error(f"(Get category by ID) Error: {e}")
            raise

    async def get_categories(self, db: Session) -> List[Category]:
        try:
            categories = db.query(Category).all()
            self.logger.info(f"(Get categories) Retrieved {len(categories)} drivers")

            return categories
        except Exception as e:
            self.logger.error(f"(Get categories) Error: {e}")
            raise