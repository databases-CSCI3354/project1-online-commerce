from flask import session

from app.models.product import Cart, CartItem


def get_cart() -> Cart:
    if "cart" not in session:
        session["cart"] = Cart(items={}).to_dict()
    return Cart.model_validate(session["cart"])


def save_item_to_cart(cart_item: CartItem) -> None:
    cart = get_cart()
    cart.items[cart_item.ProductID] = cart_item
    session["cart"] = cart.to_dict()
