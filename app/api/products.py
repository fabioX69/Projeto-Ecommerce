from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services import products_service as service

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    q: str | None = Query(None),
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    order_by_price: bool = False,
):
    return service.get_all(db, q, category, min_price, max_price, order_by_price)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return service.get_by_id(db, product_id)

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return service.create(db, payload)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    return service.update(db, product_id, payload)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return service.delete(db, product_id)

@router.get("/search/by-price", response_model=ProductOut | None)
def search_by_price(price: float, db: Session = Depends(get_db)):
    return service.search_by_price(db, price)
