from typing import Optional

from app.models.product import Product
from app.utils.database import get_db
from app.utils.logger import setup_logger

log = setup_logger(__name__)


class ProductService:

    def __init__(self):
        self.cursor = get_db().cursor()
        self.columns = list(Product.model_fields.keys())

    def get_all_products(self) -> list[Product]:
        self.cursor.execute("SELECT * FROM Products")
        products: list[Product] = [
            Product.model_validate(dict(zip(self.columns, row))) for row in self.cursor.fetchall()
        ]
        return products

    def get_product_by_id(self, product_id: Optional[int]) -> Optional[Product]:
        if product_id is None:
            return None
        self.cursor.execute("SELECT * FROM Products WHERE ProductID = ?", (product_id,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        product: Product = Product.model_validate(dict(zip(self.columns, result)))
        return product
