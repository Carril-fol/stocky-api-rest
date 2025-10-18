import uvicorn
from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv

from database.db import Database
from repositories.supplier_repository import SupplierRepository
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository

from services.supplier_service import SupplierService
from services.category_service import CategoryService
load_dotenv()

def values_init_in_database():
    supplier_repository = SupplierRepository()
    supplier_service = SupplierService(supplier_repository)

    product_repository = ProductRepository()
    category_repository = CategoryRepository()
    category_service = CategoryService(category_repository, product_repository)

    supplier_service.create_default_supplier()
    category_service.create_default_category()

def start_server(app):
    db = Database()
    db.initialize()
    values_init_in_database()

    host = app.config.get("SERVER_HOST")
    port = app.config.get("SERVER_PORT")
    app_asgi = WsgiToAsgi(app)
    uvicorn.run(app_asgi, host=host, port=port)