import pytest
from pydantic import ValidationError

from modules.users.user_orchestrator import user_service

from modules.categories.category_service import CategoryService
from modules.categories.category_repository import CategoryRepository
from modules.categories.categories_exceptions import (
    CategoryNotFound,
    CategoryNameReserved,
    CategoryStatusError,
)

from modules.products.product_repository import ProductRepository
from modules.users_companies.users_companies_repository import UsersCompaniesRepository


users_companies_repo = UsersCompaniesRepository()
category_repository = CategoryRepository()
product_repository = ProductRepository()

category_service = CategoryService(category_repository, product_repository)

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

CATEGORY_DATA = {
    "name": "Test category"
}

# --------------------------------------------------------
# Helpers
# --------------------------------------------------------

def _register_owner(user_data: dict, company_data: dict):
    user_id = user_service.register_owner(user_data, company_data)
    users_companies_data = users_companies_repo.get_user_company_role_by_user_id(user_id)
    return user_id, users_companies_data.company_id, users_companies_data.role_id

# --------------------------------------------------------
# Create
# --------------------------------------------------------

def test_create_category_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category = category_service.create_category(CATEGORY_DATA, company_id)

    assert category is not None
    assert category.name == "TEST CATEGORY"


def test_create_category_name_reserved():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(CategoryNameReserved):
        category_service.create_category({"name": "other"}, company_id)


def test_create_category_name_too_short():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(ValidationError):
        category_service.create_category({"name": "ab"}, company_id)


# --------------------------------------------------------
# Get by ID
# --------------------------------------------------------

def test_detail_category():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category_created = category_service.create_category(CATEGORY_DATA, company_id)

    category = category_service.get_category_by_id(category_created.id, company_id)

    assert category is not None
    assert category["name"] == "TEST CATEGORY"


def test_detail_category_not_found():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(CategoryNotFound):
        category_service.get_category_by_id(9999, company_id)


# --------------------------------------------------------
# Get by name
# --------------------------------------------------------

def test_get_category_by_name_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category_service.create_category(CATEGORY_DATA, company_id)

    category = category_service.get_category_by_name("test category", company_id)

    assert category is not None
    assert category["name"] == "TEST CATEGORY"


def test_get_category_by_name_not_found():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(CategoryNotFound):
        category_service.get_category_by_name("nonexistent", company_id)


# --------------------------------------------------------
# List
# --------------------------------------------------------

def test_list_categories_from_company():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category_service.create_category({"name": "Category A"}, company_id)
    category_service.create_category({"name": "Category B"}, company_id)

    categories, total = category_service.get_all_categories_from_company(company_id, page=1, per_page=10)

    assert total == 2
    assert len(categories) == 2


# --------------------------------------------------------
# Update
# --------------------------------------------------------

def test_update_category_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category_created = category_service.create_category(CATEGORY_DATA, company_id)

    category_updated = category_service.update_category(
        category_created.id,
        {"name": "Test category updated"},
        company_id,
    )

    assert category_updated is not None
    assert category_updated.name == "TEST CATEGORY UPDATED"


def test_update_category_name_too_short():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category_created = category_service.create_category(CATEGORY_DATA, company_id)

    with pytest.raises(ValidationError):
        category_service.update_category(category_created.id, {"name": ""}, company_id)


def test_update_category_not_found():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(CategoryNotFound):
        category_service.update_category(9999, {"name": "New name"}, company_id)


# --------------------------------------------------------
# Delete
# --------------------------------------------------------

def test_delete_category_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category_created = category_service.create_category(CATEGORY_DATA, company_id)

    deleted = category_service.delete_category(
        category_created.id,
        {"status": "INACTIVE"},
        company_id,
    )

    assert deleted.status == "INACTIVE"


def test_delete_category_already_inactive():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    category_created = category_service.create_category(CATEGORY_DATA, company_id)
    category_service.delete_category(category_created.id, {"status": "INACTIVE"}, company_id)

    with pytest.raises(CategoryStatusError):
        category_service.delete_category(category_created.id, {"status": "INACTIVE"}, company_id)
