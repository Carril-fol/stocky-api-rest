from flask import Flask

from asgi import start_server
from settings import settings_from_server, type_server

from controllers.product_controller import product_controller
from controllers.category_controller import category_controller
from controllers.supplier_controller import supplier_controller
from controllers.stock_controller import stock_controller
from controllers.core_controller import core_controller

# Flask
# https://flask.palletsprojects.com/en/3.0.x/
app = Flask(__name__)
app.config.from_object(settings_from_server[type_server])

# Blueprints
app.register_blueprint(product_controller)
app.register_blueprint(category_controller)
app.register_blueprint(supplier_controller)
app.register_blueprint(stock_controller)
app.register_blueprint(core_controller)

if __name__ == "__main__":
    start_server(app)