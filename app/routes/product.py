from typing import Optional

from flask import Blueprint, jsonify, render_template, request

from app.models.category import Category
from app.models.product import CartItem, Product
from app.models.supplier import Supplier
from app.services.cart import get_cart, save_item_to_cart
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.supplier import SupplierService
from app.utils.logger import setup_logger

product_bp = Blueprint("product", __name__)


log = setup_logger(__name__)


@product_bp.route("/<int:product_id>")
def index(product_id: int):
    product: Optional[Product] = ProductService().get_product_by_id(product_id)
    if not product:
        return jsonify({"error": f"Product not found with id {product_id}"}), 404
    category: Optional[Category] = CategoryService().get_category_by_id(product.CategoryID)
    supplier: Optional[Supplier] = SupplierService().get_supplier_by_id(product.SupplierID)
    return render_template(
        "product/index.html", product=product, category=category, supplier=supplier
    )


@product_bp.route("/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product: Optional[Product] = ProductService().get_product_by_id(product_id)
    if not product:
        return jsonify({"error": f"Product not found with id {product_id}"}), 404

    quantity = int(request.form.get("quantity", 1))

    if quantity > product.UnitsInStock:
        return jsonify({"error": f"Requested quantity exceeds available stock"}), 500

    cart_item = CartItem(
        ProductID=product_id,
        Quantity=quantity,
        ProductName=product.ProductName,
        TotalPrice=product.UnitPrice * quantity,
    )

    save_item_to_cart(cart_item=cart_item)
    log.info(f"Added the following item to cart: {cart_item}")

    # category: Optional[Category] = CategoryService().get_category_by_id(product.CategoryID)
    # supplier: Optional[Supplier] = SupplierService().get_supplier_by_id(product.SupplierID)
    # return render_template(
    #     "product/index.html", product=product, category=category, supplier=supplier
    # )

    return jsonify({"message": f"Added {product.ProductName} to cart"})


@product_bp.route("/checkout")
def checkout():
    cart = get_cart()
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    cart_total = sum(item.TotalPrice for item in cart.items.values())
    return render_template("product/checkout.html", cart=cart, cart_total=cart_total)

@product_bp.route("/cart")
def cart():
    cart = get_cart()
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    cart_total = sum(item.TotalPrice for item in cart.items.values())
    return render_template("product/cart.html", cart=cart, cart_total=cart_total)
