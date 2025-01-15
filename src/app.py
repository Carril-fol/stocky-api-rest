from flask import Flask

from asgi import start_server
from settings import settings_from_server, type_server
from utils.extensions import jwt
from controllers.product_controller import product_controller
from controllers.category_controller import category_controller
from controllers.supplier_controller import supplier_controller

# Flask
# https://flask.palletsprojects.com/en/3.0.x/
app = Flask(__name__)
app.config.from_object(settings_from_server[type_server])

# Blueprints
app.register_blueprint(product_controller)
app.register_blueprint(category_controller)
app.register_blueprint(supplier_controller)

# Extensions
jwt.init_app(app)

if __name__ == "__main__":
    start_server(app)