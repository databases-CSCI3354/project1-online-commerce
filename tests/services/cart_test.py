import pytest
from flask import session

from app.models.product import Cart, CartItem
from app.services.cart import get_cart, save_item_to_cart


def test_get_cart_creates_new_cart(client):
    with client:
        client.get("/")  # This will create a session
        cart = get_cart()
        assert isinstance(cart, Cart)
        assert cart.items == {}
        assert session["cart"] == Cart(items={})


def test_get_cart_returns_existing_cart(client):
    with client:
        client.get("/")  # This will create a session
        existing_cart = Cart(
            items={1: CartItem(ProductID=1, ProductName="Product 1", Quantity=2, TotalPrice=10)}
        )
        session["cart"] = existing_cart.model_dump()

        cart = get_cart()
        assert isinstance(cart, Cart)
        assert cart.items[1].ProductID == 1
        assert cart.items[1].Quantity == 2


def test_save_item_to_cart(client):
    with client:
        client.get("/")  # This will create a session
        cart_item = CartItem(ProductID=123, ProductName="Product 1", Quantity=2, TotalPrice=10)
        save_item_to_cart(cart_item)

        saved_cart = Cart.model_validate(session["cart"])
        assert saved_cart.items[123].ProductID == 123
        assert saved_cart.items[123].Quantity == 2
        assert saved_cart.items[123].ProductName == "Product 1"
        assert saved_cart.items[123].TotalPrice == 10


def test_save_item_updates_existing_cart(client):
    with client:
        client.get("/")  # This will create a session
        save_item_to_cart(
            CartItem(ProductID=123, ProductName="Product 1", Quantity=2, TotalPrice=10)
        )
        save_item_to_cart(
            CartItem(ProductID=1234, ProductName="Product 1", Quantity=3, TotalPrice=10)
        )

        saved_cart = Cart.model_validate(session["cart"])
        assert len(saved_cart.items) == 2
        assert saved_cart.items[123].Quantity == 2
        assert saved_cart.items[1234].Quantity == 3
