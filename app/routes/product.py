from typing import Optional

from flask import Blueprint, render_template

from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier
from app.services.category import CategoryService
from app.services.products import ProductService
from app.services.supplier import SupplierService

product_bp = Blueprint("product", __name__)


@product_bp.route("/<int:product_id>")
def index(product_id: int):
    product: Product = ProductService().get_product_by_id(product_id)
    category: Optional[Category] = CategoryService().get_category_by_id(product.CategoryID)
    supplier: Optional[Supplier] = SupplierService().get_supplier_by_id(product.SupplierID)
    return render_template(
        "product/index.html", product=product, category=category, supplier=supplier
    )
