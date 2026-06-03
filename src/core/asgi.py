from .database import Database

from modules.users.user_entity import UserEntity
from modules.products.product_entity import ProductEntity
from modules.categories.category_entity import CategoryEntity
from modules.suppliers.supplier_entity import SupplierEntity
from modules.stock.stock_entity import StockEntity
from modules.companies.company_entity import CompanyEntity
from modules.roles.role_entity import RoleEntity
from modules.users_companies.users_companies_entity import UsersCompaniesEntity
from modules.permissions.permissions_entity import PermissionsEntity

from seeds.permissions_seeder import seed_permissions

def start_server(app):
    db = Database()
    db.initialize(create_tables=True)

    seed_permissions()
    app.run(host="0.0.0.0", port=8000, debug=True)