from typing import Optional

from app.models.category import Category
from app.utils.database import get_db


class CategoryService:

    def __init__(self):
        self.cursor = get_db().cursor()
        self.columns = list(Category.model_fields.keys())

    def get_category_by_id(self, category_id: Optional[int]) -> Optional[Category]:
        if category_id is None:
            return None
        self.cursor.execute("SELECT * FROM Categories WHERE CategoryID = ?", (category_id,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        category: Category = Category.model_validate(dict(zip(self.columns, result)))
        return category
