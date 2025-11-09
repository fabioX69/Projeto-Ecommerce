from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    category: str = ""
    price: float = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True
