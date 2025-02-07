from flask import session

from app.models.product import Cart


def get_cart() -> Cart:
    return Cart.model_validate(session.get("cart", {}))


def save_cart(cart: Cart):
    session["cart"] = cart.model_dump()

