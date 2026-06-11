import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dotenv import load_dotenv
load_dotenv()

from core.database import Base

# Import every entity so autogenerate sees the full schema.
# Missing an entity here causes autogenerate to emit a spurious DROP TABLE.
from modules.users.user_entity import UserEntity
from modules.companies.company_entity import CompanyEntity
from modules.roles.role_entity import RoleEntity
from modules.permissions.permissions_entity import PermissionsEntity
from modules.role_permissions.role_permissions_entity import RolePermissionEntity
from modules.users_companies.users_companies_entity import UsersCompaniesEntity
from modules.categories.category_entity import CategoryEntity
from modules.products.product_entity import ProductEntity
from modules.stock.stock_entity import StockEntity

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    url = os.getenv("NEON_DATABASE_URL")
    if not url:
        raise RuntimeError("NEON_DATABASE_URL is not set in the environment.")
    return url


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(get_url(), poolclass=pool.NullPool, future=True)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
