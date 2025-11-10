from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

# ---------- Algoritmos ----------
def merge_sort(items, key=lambda x: x):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def binary_search(items, target, key=lambda x: x):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        value = key(items[mid])
        if value == target:
            return items[mid]
        elif value < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

# ---------- CRUD ----------
def get_all(db: Session, q=None, category=None, min_price=None, max_price=None, order_by_price=False):
    stmt = select(Product)
    if q:
        stmt = stmt.where(Product.name.ilike(f"%{q}%"))
    if category:
        stmt = stmt.where(Product.category == category)
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)
    items = db.execute(stmt).scalars().all()
    return merge_sort(items, key=lambda p: p.price) if order_by_price else items

def get_by_id(db: Session, product_id: int):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

def create(db: Session, data: ProductCreate):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update(db: Session, product_id: int, data: ProductUpdate):
    product = get_by_id(db, product_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

def delete(db: Session, product_id: int):
    product = get_by_id(db, product_id)
    db.delete(product)
    db.commit()
    return {"detail": "Produto removido com sucesso"}

def search_by_price(db: Session, price: float):
    items = db.execute(select(Product)).scalars().all()
    items_sorted = merge_sort(items, key=lambda p: p.price)
    return binary_search(items_sorted, price, key=lambda p: p.price)
