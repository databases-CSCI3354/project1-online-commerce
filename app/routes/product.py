from typing import Optional

from flask import Blueprint, jsonify, render_template

from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.supplier import SupplierService

product_bp = Blueprint("product", __name__)
product_service = ProductService()
category_service = CategoryService()
supplier_service = SupplierService()


@product_bp.route("/<int:product_id>", methods=["GET"])
def index(product_id: int):
    product: Optional[Product] = product_service.get_product_by_id(product_id)
    if not product:
        raise ValueError(f"Error rendering product page: product not found with id {product_id}")

    category: Optional[Category] = category_service.get_category_by_id(product.CategoryID)
    supplier: Optional[Supplier] = supplier_service.get_supplier_by_id(product.SupplierID)
    return render_template(
        "product/index.html", product=product, category=category, supplier=supplier
    )


@product_bp.route("/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product: Optional[Product] = product_service.get_product_by_id(product_id)
    if not product:
        raise ValueError(f"Error adding product to cart: product not found with id {product_id}")

    # quantity = int(request.form.get("quantity", 1))

    # if quantity > product.UnitsInStock:
    #     return jsonify({"message": "Requested quantity exceeds available stock"}), 400

    # cart = session.get("cart", {})
    # cart[product_id] = cart.get(product_id, 0) + quantity
    # session["cart"] = cart

    return jsonify({"message": f"Added {product.ProductName} to cart"})
