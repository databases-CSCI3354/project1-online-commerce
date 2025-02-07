from flask import Blueprint, render_template

from app.models.product import Product
from app.services.products import ProductService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Main landing page"""
    products: list[Product] = ProductService().get_all_products()
    return render_template("main/index.html", products=products)
