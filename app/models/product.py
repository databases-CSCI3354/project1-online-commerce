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

    def to_dict(self):
        return {
            "ProductID": self.ProductID,
            "ProductName": self.ProductName,
            "SupplierID": self.SupplierID,
            "CategoryID": self.CategoryID,
            "QuantityPerUnit": self.QuantityPerUnit,
            "UnitPrice": self.UnitPrice,
            "UnitsInStock": self.UnitsInStock,
            "UnitsOnOrder": self.UnitsOnOrder,
            "ReorderLevel": self.ReorderLevel,
            "Discontinued": self.Discontinued,
        }


class CartItem(BaseModel):
    ProductID: int
    Quantity: int
    ProductName: str
    TotalPrice: float

    def to_dict(self):
        return {
            "ProductID": self.ProductID,
            "Quantity": self.Quantity,
            "ProductName": self.ProductName,
            "TotalPrice": self.TotalPrice,
        }


class Cart(BaseModel):
    items: dict[int, CartItem]

    def to_dict(self):
        return {"items": {k: v.to_dict() for k, v in self.items.items()}}
