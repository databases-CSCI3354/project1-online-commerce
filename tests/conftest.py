from unittest.mock import Mock, patch

import pytest
from flask import g

from app import create_app
from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.supplier import SupplierService


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def mock_cursor():
    cursor = Mock()
    return cursor


@pytest.fixture
def mock_db(app, mock_cursor):
    with app.app_context():
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the database connection
        with patch("app.utils.database.get_db", return_value=mock_conn):
            g.db = mock_conn
            yield mock_cursor


@pytest.fixture
def mock_category_service(mock_db):
    service = CategoryService()
    # Ensure the cursor is set after initialization
    service.cursor = mock_db
    return service


@pytest.fixture
def mock_product_service(mock_db):
    service = ProductService()
    # Ensure the cursor is set after initialization
    service.cursor = mock_db
    return service


@pytest.fixture
def mock_supplier_service(mock_db):
    service = SupplierService()
    # Ensure the cursor is set after initialization
    service.cursor = mock_db
    return service


# DO NOT CHANGE THIS FIXTURE AS ITS VALUE IS USED IN MANY TESTS
@pytest.fixture
def mock_product():
    return Product(
        ProductID=1,
        ProductName="Test Product",
        CategoryID=1,
        SupplierID=1,
        QuantityPerUnit="10 boxes",
        UnitPrice=10.0,
        UnitsInStock=100,
        UnitsOnOrder=0,
        ReorderLevel=0,
        Discontinued="1",
    )


# DO NOT CHANGE THIS FIXTURE AS ITS VALUE IS USED IN MANY TESTS
@pytest.fixture
def mock_category():
    return Category(
        CategoryID=1,
        CategoryName="Test Category",
        Description="Test Category Description",
        Picture=b"Test Category Picture",
    )


# DO NOT CHANGE THIS FIXTURE AS ITS VALUE IS USED IN MANY TESTS
@pytest.fixture
def mock_supplier():
    return Supplier(
        SupplierID=1,
        CompanyName="Test Company",
        ContactName="Test Contact",
        ContactTitle="Test Contact Title",
        Address="Test Address",
        City="Test City",
        Region="Test Region",
        PostalCode="Test Postal Code",
        Country="Test Country",
        Phone="Test Phone",
        Fax="Test Fax",
        HomePage="Test Home Page",
    )
