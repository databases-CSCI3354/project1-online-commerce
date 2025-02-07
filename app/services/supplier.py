from typing import Optional

from app.models.supplier import Supplier
from app.utils.database import get_db


class SupplierService:
    def __init__(self):
        self.cursor = get_db().cursor()
        self.columns = list(Supplier.model_fields.keys())

    def get_supplier_by_id(self, supplier_id: Optional[int]) -> Optional[Supplier]:
        if not supplier_id:
            return None
        self.cursor.execute(f"SELECT * FROM Suppliers WHERE SupplierID = {supplier_id}")
        supplier: Supplier = Supplier.model_validate(
            dict(zip(self.columns, self.cursor.fetchone()))
        )
        return supplier
