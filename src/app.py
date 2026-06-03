from core.asgi import start_server
from core.extensions import app, spectree
from core.settings import settings_from_server, type_server
from core.health import health_blueprint

from modules.products.product_controller import product_controller
from modules.categories.category_controller import category_controller
from modules.stock.stock_controller import stock_blueprint
from modules.companies.company_controller import company_controller
from modules.users.user_controller import users_blueprint
from modules.users_companies.users_companies_controller import users_companies_blueprint
from modules.roles.role_controller import role_blueprint
from modules.role_permissions.role_permission_controller import role_permission_controller

#Spectree
spectree.register(app)

# Flask
# https://flask.palletsprojects.com/en/3.0.x/
app.config.from_object(settings_from_server[type_server])

# Blueprints
app.register_blueprint(product_controller)
app.register_blueprint(category_controller)
app.register_blueprint(stock_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(users_companies_blueprint)
app.register_blueprint(company_controller)
app.register_blueprint(role_blueprint)
app.register_blueprint(role_permission_controller)
app.register_blueprint(health_blueprint)

if __name__ == "__main__":
    start_server(app)