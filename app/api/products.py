from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
import heapq

router = APIRouter(prefix="/products", tags=["products"])

def _merge_sort(items, key=lambda x: x):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = _merge_sort(items[:mid], key)
    right = _merge_sort(items[mid:], key)
    return _merge(left, right, key)

def _merge(left, right, key):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out

def _binary_search(items, target, key=lambda x: x):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        k = key(items[mid])
        if k == target: return items[mid]
        if k < target: low = mid + 1
        else: high = mid - 1
    return None

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    obj = Product(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    q: str | None = Query(None),
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    order_by_price: bool = False,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
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
    if order_by_price:
        items = _merge_sort(items, key=lambda p: p.price)
    return items[offset:offset+limit]

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.get(Product, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return obj

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    obj = db.get(Product, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.get(Product, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(obj)
    db.commit()
    return None

@router.get("/search/by-price", response_model=ProductOut | None, tags=["algorithms"])
def search_by_price(price: float, db: Session = Depends(get_db)):
    items = db.execute(select(Product)).scalars().all()
    items_sorted = _merge_sort(items, key=lambda p: p.price)
    return _binary_search(items_sorted, price, key=lambda p: p.price)

@router.get("/topn/by-price", response_model=list[ProductOut], tags=["algorithms"])
def topn_by_price(n: int = Query(5, ge=1, le=100), db: Session = Depends(get_db)):
    items = db.execute(select(Product)).scalars().all()
    heap: list[tuple[float, Product]] = []
    for p in items:
        if len(heap) < n:
            heapq.heappush(heap, (p.price, p))
        else:
            if p.price > heap[0][0]:
                heapq.heapreplace(heap, (p.price, p))
    return [pair[1] for pair in sorted(heap, key=lambda t: t[0], reverse=True)]
