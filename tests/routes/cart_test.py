import pytest
from flask import url_for

from app.models.product import Product
from app.services.cart import CartService
from app.services.product import ProductService


@pytest.fixture
def mock_product():
    return Product(
        ProductID=1,
        ProductName="Chai",
        SupplierID=1,
        CategoryID=1,
        QuantityPerUnit="10 boxes x 20 bags",
        UnitPrice=18.00,
        UnitsInStock=39,
        UnitsOnOrder=0,
        ReorderLevel=10,
        Discontinued="0",
    )


@pytest.fixture
def mock_product_service(mock_product):
    class MockProductService:
        def get_product_by_id(self, product_id):
            if product_id == mock_product.ProductID:
                return mock_product
            return None

    return MockProductService()


@pytest.fixture
def mock_cart_service():
    class MockCartService:
        def __init__(self):
            self.cart_items = {}
        
        def add_to_cart(self, product_id, quantity):
            if product_id in self.cart_items:
                self.cart_items[product_id] += quantity
            else:
                self.cart_items[product_id] = quantity
        
        def get_cart_items(self):
            from app.models.cart import CartItem
            items = []
            for product_id, quantity in self.cart_items.items():
                items.append(
                    CartItem(
                        ProductID=product_id,
                        Quantity=quantity,
                        ProductName=f"Product {product_id}",
                        TotalPrice=quantity * 18.00,  # Using a fixed price for simplicity
                    )
                )
            return items
        
        def get_item_quantity(self, product_id):
            return self.cart_items.get(product_id, 0)
        
        def remove_from_cart(self, product_id):
            if product_id in self.cart_items:
                del self.cart_items[product_id]

    return MockCartService()


def test_add_to_cart(client, mock_product_service, mock_cart_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(ProductService, "get_product_by_id", mock_product_service.get_product_by_id)
    monkeypatch.setattr(CartService, "get_item_quantity", mock_cart_service.get_item_quantity)
    monkeypatch.setattr(CartService, "add_to_cart", mock_cart_service.add_to_cart)
    
    # Test adding a product to the cart
    response = client.post(f"/product/1", data={"quantity": 2})
    
    # Check redirect
    assert response.status_code == 302
    assert "/product/1" in response.headers["Location"]
    
    # Follow redirect and check for success message
    response = client.get("/product/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Added 2 Chai to cart!" in response.data


def test_add_to_cart_exceeding_stock(client, mock_product_service, mock_cart_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(ProductService, "get_product_by_id", mock_product_service.get_product_by_id)
    monkeypatch.setattr(CartService, "get_item_quantity", mock_cart_service.get_item_quantity)
    
    # Try to add more than available stock
    response = client.post(f"/product/1", data={"quantity": 40})  # Stock is 39
    
    # Check redirect
    assert response.status_code == 302
    
    # Follow redirect and check for error message
    response = client.get("/product/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot add 40 items" in response.data


def test_view_cart(client, mock_cart_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(CartService, "get_cart_items", mock_cart_service.get_cart_items)
    
    # Add items to the cart
    mock_cart_service.add_to_cart(1, 2)  # 2 of product 1
    mock_cart_service.add_to_cart(2, 3)  # 3 of product 2
    
    # Test viewing the cart
    response = client.get("/product/checkout")
    assert response.status_code == 200
    
    # Check if cart items are displayed
    assert b"Product 1" in response.data
    assert b"Product 2" in response.data
    assert b"2" in response.data  # Quantity of product 1
    assert b"3" in response.data  # Quantity of product 2
    
    # Check if total price is displayed
    # Total: (2 * 18.00) + (3 * 18.00) = 36.00 + 54.00 = 90.00
    assert b"90.00" in response.data


def test_remove_from_cart(client, mock_cart_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(CartService, "get_cart_items", mock_cart_service.get_cart_items)
    monkeypatch.setattr(CartService, "remove_from_cart", mock_cart_service.remove_from_cart)
    
    # Add items to the cart
    mock_cart_service.add_to_cart(1, 2)  # 2 of product 1
    mock_cart_service.add_to_cart(2, 3)  # 3 of product 2
    
    # Test removing an item from the cart
    response = client.post("/product/cart/remove/1")
    
    # Check redirect
    assert response.status_code == 302
    assert "/product/checkout" in response.headers["Location"]
    
    # Follow redirect and check for success message
    response = client.get("/product/checkout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Item removed from cart successfully!" in response.data
    
    # Check if the removed item is no longer in the cart
    assert b"Product 1" not in response.data
    assert b"Product 2" in response.data 