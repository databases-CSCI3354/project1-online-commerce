from pydantic import BaseModel


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
        return {k: v.to_dict() for k, v in self.items.items()} 
