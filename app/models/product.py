from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    ProductID: int
    ProductName: str
    SupplierID: int
    CategoryID: int
    QuantityPerUnit: str
    UnitPrice: float
    UnitsInStock: int
    UnitsOnOrder: int
    ReorderLevel: int
    Discontinued: str


class CartItem(BaseModel):
    ProductID: int
    Quantity: int
    ProductName: str
    TotalPrice: float


class Cart(BaseModel):
    items: dict[int, CartItem]
