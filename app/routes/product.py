from typing import Optional

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.wrappers.response import Response

from app.models.cart import CartItem
from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier
from app.services.cart import CartService, get_cart, save_item_to_cart
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
def add_to_cart(product_id) -> Response:
    product: Optional[Product] = ProductService().get_product_by_id(product_id)
    if not product:
        flash(f"Product not found with id {product_id}", "error")
        return redirect(url_for("main.index"))

    quantity = int(request.form.get("quantity", 1))

    # get the current quantity of the product in the cart to avoid adding more than the stock
    cart_service = CartService()
    current_cart_quantity = cart_service.get_item_quantity(product_id)
    total_quantity = current_cart_quantity + quantity

    if total_quantity > product.UnitsInStock:
        flash(
            f"Cannot add {quantity} items. Only {product.UnitsInStock - current_cart_quantity} remaining.",
            "error",
        )
        return redirect(url_for("product.index", product_id=product_id))

    cart_item = CartItem(
        ProductID=product_id,
        Quantity=quantity,
        ProductName=product.ProductName,
        TotalPrice=product.UnitPrice * quantity,
    )

    save_item_to_cart(cart_item=cart_item)
    log.info(f"Added the following item to cart: {cart_item}")

    flash(f"Added {quantity} {product.ProductName} to cart!", "success")
    return redirect(url_for("product.index", product_id=product_id))


@product_bp.route("/checkout")
def checkout():
    cart = get_cart()
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    cart_total = sum(item.TotalPrice for item in cart.items.values())
    return render_template("product/checkout.html", cart=cart, cart_total=cart_total)


@product_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_service = CartService()
    cart_service.remove_from_cart(product_id)
    flash("Item removed from cart successfully!", "success")
    return redirect(url_for("product.checkout"))
