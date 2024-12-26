from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db_items
from src.models.item import Item
from src.schemas.item import ItemSchema

router = APIRouter()

@router.get("/items/{item_id}", response_model=ItemSchema)
def get_item_by_id(item_id: int, db: Session = Depends(get_db_items)):
    # Проверяем наличие товара по ID
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
