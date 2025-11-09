from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    category: Mapped[str] = mapped_column(String(60), index=True, default="")
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
