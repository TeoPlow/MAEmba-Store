from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db_items
from src.models.item_category import ItemCategory
from src.models.items import Items

router = APIRouter(prefix="/api/items", tags=["Items"])

# Получение всех категорий
@router.get("/categories", response_model=list[dict])
def get_all_categories(db: Session = Depends(get_db_items)):
    categories = db.query(ItemCategory).all()
    return [{"id": category.item_category_id, "name": category.item_category_name} for category in categories]

# Получение категории по ID
@router.get("/categories/{category_id}", response_model=dict)
def get_category_by_id(category_id: str, db: Session = Depends(get_db_items)):
    category = db.query(ItemCategory).filter(ItemCategory.item_category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {
        "id": category.item_category_id,
        "name": category.item_category_name,
        "subcategories": [
            {"id": sub.item_category_id, "name": sub.item_category_name} 
            for sub in category.subcategories
        ]
    }

# Получение всех товаров
@router.get("/items", response_model=list[dict])
def get_all_items(db: Session = Depends(get_db_items)):
    items = db.query(Items).all()
    return [{"id": item.item_id, "name": item.item_name, "category_id": item.item_category_id} for item in items]

# Получение товара по ID
@router.get("/items/{item_id}", response_model=dict)
def get_item_by_id(item_id: str, db: Session = Depends(get_db_items)):
    item = db.query(Items).filter(Items.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "id": item.item_id,
        "name": item.item_name,
        "category_id": item.item_category_id,
    }

# Получение всех товаров в категории
@router.get("/categories/{category_id}/items", response_model=list[dict])
def get_items_by_category(category_id: str, db: Session = Depends(get_db_items)):
    category = db.query(ItemCategory).filter(ItemCategory.item_category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return [
        {"id": item.item_id, "name": item.item_name} 
        for item in category.items
    ]
