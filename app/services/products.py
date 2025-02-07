from app.models.product import Product
from app.utils.database import get_db


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

    def get_product_by_id(self, product_id: int) -> Product:
        self.cursor.execute(f"SELECT * FROM Products WHERE ProductID = {product_id}")
        product: Product = Product.model_validate(dict(zip(self.columns, self.cursor.fetchone())))
        return product
