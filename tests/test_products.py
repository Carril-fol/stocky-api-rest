import pytest

from modules.users.user_orchestrator import user_service
from modules.users_companies.users_companies_repository import UsersCompaniesRepository

from modules.products.product_service import ProductService
from modules.products.product_repository import ProductRepository
from modules.products.products_exceptions import ProductNotFound, ProductHasAlreadyStatus

from modules.categories.category_service import CategoryService
from modules.categories.category_repository import CategoryRepository

from modules.stock.stock_repository import StockRepository

users_companies_repo = UsersCompaniesRepository()
category_service = CategoryService(CategoryRepository(), ProductRepository())
product_repository = ProductRepository()
stock_repository = StockRepository()
product_service = ProductService(product_repository, stock_repository)

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

def _create_category(company_id: int, name: str = "Electronics"):
    return category_service.create_category({"name": name}, company_id)

def _create_product(company_id: int, category_id: int, name: str = "Test Product", quantity: int = 5):
    data = {
        "name": name,
        "description": "A test product",
        "category_id": category_id,
        "quantity": quantity,
    }
    return product_service.create_product(data, company_id)

# --------------------------------------------------------
# Create
# --------------------------------------------------------

def test_create_product_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)

    product = _create_product(company_id, category.id)

    assert product is not None
    assert product.name == "TEST PRODUCT"
    assert product.company_id == company_id
    assert product.status == "ACTIVE"


def test_create_product_creates_stock():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    product = _create_product(company_id, category.id)

    stock = stock_repository.get_stock_by_product_id(product.id)
    assert stock is not None
    assert stock.product_id == product.id


# --------------------------------------------------------
# Get
# --------------------------------------------------------

def test_get_product_by_id_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    product = _create_product(company_id, category.id)

    result = product_service.get_product_by_id(product.id)

    assert result["id"] == product.id


def test_get_product_by_id_not_found():
    with pytest.raises(ProductNotFound):
        product_service.get_product_by_id(99999)


def test_get_product_by_name_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    _create_product(company_id, category.id, name="Unique Product")

    result = product_service.get_product_by_name("Unique Product", company_id)

    assert result is not None
    assert result["name"] == "UNIQUE PRODUCT"


def test_get_product_by_name_not_found():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(ProductNotFound):
        product_service.get_product_by_name("nonexistent", company_id)


def test_get_all_products():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    _create_product(company_id, category.id, name="Product A")
    _create_product(company_id, category.id, name="Product B")

    products, total = product_service.get_products(company_id, page=1, per_page=10)

    assert total == 2
    assert len(products) == 2


# --------------------------------------------------------
# Update
# --------------------------------------------------------

def test_update_product_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    product = _create_product(company_id, category.id)

    product_service.update_product(product.id, {"name": "Updated Name"})
    result = product_service.get_product_by_id(product.id)

    assert result["name"] == "UPDATED NAME"


def test_update_product_not_found():
    with pytest.raises(ProductNotFound):
        product_service.update_product(99999, {"name": "New Name"})


# --------------------------------------------------------
# Deactivate
# --------------------------------------------------------

def test_deactivate_product_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    product = _create_product(company_id, category.id)

    product_service.deactivate_product(product.id, {"status": "INACTIVE"})
    result = product_service.get_product_by_id(product.id)

    assert result["status"] == "INACTIVE"


def test_deactivate_product_already_inactive():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    product = _create_product(company_id, category.id)

    product_service.deactivate_product(product.id, {"status": "INACTIVE"})

    with pytest.raises(ProductHasAlreadyStatus):
        product_service.deactivate_product(product.id, {"status": "INACTIVE"})


def test_deactivate_product_zeros_stock():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = _create_category(company_id)
    product = _create_product(company_id, category.id, quantity=10)

    product_service.deactivate_product(product.id, {"status": "INACTIVE"})
    stock = stock_repository.get_stock_by_product_id(product.id)

    assert stock.quantity == 0


# --------------------------------------------------------
# Multi-tenant isolation
# --------------------------------------------------------

def test_products_isolated_between_companies():
    _, company_a_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, company_b_id, _ = _register_owner(
        {**USER_DATA, "email": "owner_b@test.com"},
        {**COMPANY_DATA, "name": "Company B"},
    )

    category_a = _create_category(company_a_id)
    _create_product(company_a_id, category_a.id)

    products_b, total = product_service.get_products(company_b_id, page=1, per_page=10)

    assert total == 0
    assert len(products_b) == 0


def test_get_product_by_name_isolated_between_companies():
    _, company_a_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, company_b_id, _ = _register_owner(
        {**USER_DATA, "email": "owner_b@test.com"},
        {**COMPANY_DATA, "name": "Company B"},
    )

    category_a = _create_category(company_a_id)
    _create_product(company_a_id, category_a.id, name="Secret Product")

    with pytest.raises(ProductNotFound):
        product_service.get_product_by_name("Secret Product", company_b_id)
