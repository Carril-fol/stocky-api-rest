import pytest
from pydantic import ValidationError

from modules.users.user_orchestrator import user_service
from modules.users_companies.users_companies_repository import UsersCompaniesRepository

from modules.categories.category_service import CategoryService
from modules.categories.category_repository import CategoryRepository

from modules.products.product_service import ProductService
from modules.products.product_repository import ProductRepository

from modules.stock.stock_service import StockService
from modules.stock.stock_repository import StockRepository
from modules.stock.stock_exceptions import StockNotFound
from modules.stock.stock_model import derive_stock_status

users_companies_repo = UsersCompaniesRepository()
category_service = CategoryService(CategoryRepository(), ProductRepository())
product_repository = ProductRepository()
stock_repository = StockRepository()
product_service = ProductService(product_repository, stock_repository)
stock_service = StockService(stock_repository, product_repository)

# --------------------------------------------------------
# Data
# --------------------------------------------------------

USER_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
}

COMPANY_DATA = {
    "name": "Test Corp",
    "country": "Argentina",
    "address": "123 Main St",
}

# --------------------------------------------------------
# Helpers
# --------------------------------------------------------

def _register_owner(user_data: dict, company_data: dict):
    user_id = user_service.register_owner(user_data, company_data)
    uc = users_companies_repo.get_user_company_role_by_user_id(user_id)
    return user_id, uc.company_id, uc.role_id

def _create_product(company_id: int, name: str = "Test Product", quantity: int = 5):
    category = category_service.create_category({"name": "Electronics"}, company_id)
    return product_service.create_product(
        {"name": name, "description": "A test product", "category_id": category.id, "quantity": quantity},
        company_id,
    )


# --------------------------------------------------------
# derive_stock_status
# --------------------------------------------------------

def test_status_out_of_stock():
    assert derive_stock_status(0) == "OUT OF STOCK"

def test_status_out_of_stock_negative():
    assert derive_stock_status(-1) == "OUT OF STOCK"

def test_status_low_stock():
    assert derive_stock_status(5) == "LOW STOCK"

def test_status_in_stock():
    assert derive_stock_status(10) == "IN STOCK"

def test_status_in_stock_boundary():
    assert derive_stock_status(9) == "LOW STOCK"


# --------------------------------------------------------
# Get by ID
# --------------------------------------------------------

def test_get_stock_by_id_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    product = _create_product(company_id)
    stock = stock_repository.get_stock_by_product_id(product.id)

    result = stock_service.get_stock_by_id(stock.id)

    assert result["stock"]["id"] == stock.id
    assert result["product"]["id"] == product.id


def test_get_stock_by_id_not_found():
    with pytest.raises(StockNotFound):
        stock_service.get_stock_by_id(99999)


# --------------------------------------------------------
# Update
# --------------------------------------------------------

def test_update_stock_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    product = _create_product(company_id, quantity=5)
    stock = stock_repository.get_stock_by_product_id(product.id)

    stock_service.update_stock(stock.id, {"quantity": 20})
    updated = stock_repository.get_stock_by_id(stock.id)

    assert updated.quantity == 20


def test_update_stock_not_found():
    with pytest.raises(StockNotFound):
        stock_service.update_stock(99999, {"quantity": 10})


def test_update_stock_negative_quantity():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    product = _create_product(company_id)
    stock = stock_repository.get_stock_by_product_id(product.id)

    with pytest.raises(ValidationError):
        stock_service.update_stock(stock.id, {"quantity": -1})


# --------------------------------------------------------
# Detailed listing
# --------------------------------------------------------

def test_get_stock_detailed_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _create_product(company_id, name="Product A", quantity=10)
    _create_product(company_id, name="Product B", quantity=20)

    stocks, total = stock_service.get_stock_detailed_with_product(page=1, per_page=10, company_id=company_id)

    assert total == 2
    assert len(stocks) == 2


def test_get_stock_detailed_excludes_inactive_products():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    active = _create_product(company_id, name="Active Product", quantity=10)
    inactive = _create_product(company_id, name="Inactive Product", quantity=5)

    product_service.deactivate_product(inactive.id, {"status": "INACTIVE"})

    stocks, total = stock_service.get_stock_detailed_with_product(page=1, per_page=10, company_id=company_id)

    assert total == 1
    assert stocks[0]["product"]["id"] == active.id


# --------------------------------------------------------
# Low stock
# --------------------------------------------------------

def test_get_stock_low_returns_low_and_out_of_stock():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _create_product(company_id, name="Full Product", quantity=15)
    _create_product(company_id, name="Low Product", quantity=3)
    _create_product(company_id, name="Empty Product", quantity=0)

    low_stocks, total = stock_service.get_stock_low(page=1, per_page=10, company_id=company_id)

    assert total == 2
    quantities = [item["stock"]["quantity"] for item in low_stocks]
    assert all(q < 10 for q in quantities)


def test_get_stock_low_excludes_inactive_products():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    low_active = _create_product(company_id, name="Low Active", quantity=3)
    low_inactive = _create_product(company_id, name="Low Inactive", quantity=2)

    product_service.deactivate_product(low_inactive.id, {"status": "INACTIVE"})

    low_stocks, total = stock_service.get_stock_low(page=1, per_page=10, company_id=company_id)

    assert total == 1
    assert low_stocks[0]["product"]["id"] == low_active.id


# --------------------------------------------------------
# Tenant isolation
# --------------------------------------------------------

def test_stock_isolated_between_companies():
    _, company_a_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, company_b_id, _ = _register_owner(
        {**USER_DATA, "email": "owner_b@test.com"},
        {**COMPANY_DATA, "name": "Company B"},
    )

    _create_product(company_a_id, quantity=10)

    stocks_b, total = stock_service.get_stock_detailed_with_product(page=1, per_page=10, company_id=company_b_id)

    assert total == 0
    assert len(stocks_b) == 0
