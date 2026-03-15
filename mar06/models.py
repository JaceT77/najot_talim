from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    products: Mapped[List["Product"]] = relationship(back_populates='category', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.id!r}. {self.name!r}"
    

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates='products')

    def __repr__(self) -> str:
        return f"{self.id!r}. {self.name!r}. {self.category.name!r}"
    
