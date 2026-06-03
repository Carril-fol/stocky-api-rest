import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.database import Database, Base
from core.extensions import app as flask_app

from modules.users.user_entity import UserEntity
from modules.companies.company_entity import CompanyEntity
from modules.roles.role_entity import RoleEntity
from modules.users_companies.users_companies_entity import UsersCompaniesEntity
from modules.permissions.permissions_entity import PermissionsEntity
from modules.role_permissions.role_permissions_entity import RolePermissionEntity
from modules.categories.category_entity import CategoryEntity
from modules.products.product_entity import ProductEntity
from modules.stock.stock_entity import StockEntity
from modules.suppliers.supplier_entity import SupplierEntity

_test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
Database._engine = _test_engine
Database._SessionLocal = sessionmaker(
    bind=_test_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)
Base.metadata.create_all(bind=_test_engine)

flask_app.config.update({
    "TESTING": True,
    "JWT_SECRET_KEY": "test-secret-key",
    "JWT_TOKEN_LOCATION": ["headers"],
    "JWT_COOKIE_CSRF_PROTECT": False,
    "JWT_HEADER_NAME": "Authorization",
    "JWT_HEADER_TYPE": "Bearer",
})

from seeds.permissions_seeder import seed_permissions


@pytest.fixture(scope="session")
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db():
    with Database.session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
    seed_permissions()
    yield
