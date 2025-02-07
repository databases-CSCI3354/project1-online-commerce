from typing import Optional

from app.models.product import Product
from app.utils.database import get_db
# from app.utils.logger import setup_logger

# log = setup_logger("ProductService")


class ProductService:

    def __init__(self):
        self.cursor = None
        self.columns = list(Product.model_fields.keys())

        
    def _ensure_cursor(self):
        if self.cursor is None:
            self.cursor = get_db().cursor()
        return self.cursor

    def get_all_products(self) -> list[Product]:
        cursor = self._ensure_cursor()
        cursor.execute("SELECT * FROM Products")
        products: list[Product] = [
            Product.model_validate(dict(zip(self.columns, row))) for row in cursor.fetchall()
        ]
        return products

    def get_product_by_id(self, product_id: Optional[int]) -> Optional[Product]:
        if not product_id:
            return None
        cursor = self._ensure_cursor()
        cursor.execute(f"SELECT * FROM Products WHERE ProductID = {product_id}")
        rows: list = cursor.fetchall()
        match len(rows):
            case 0:
                log.info(f"No product found with id {product_id}")
                return None
            case 1:
                product: Product = Product.model_validate(dict(zip(self.columns, rows[0])))
                return product
            case _:
                log.error(
                    f"Invalid number of rows returned for product with id {product_id}: {len(rows)}"
                )
                raise ValueError("Multiple rows returned")
