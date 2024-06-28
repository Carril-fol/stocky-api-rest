from flask import Flask
from flask_jwt_extended import JWTManager

from .users.controllers.userControllers import userBlueprint
from .products.controllers.productsControllers import productBlueprint

# Flask
# https://flask.palletsprojects.com/en/3.0.x/

app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Flask-JWT-Extended
# https://flask-jwt-extended.readthedocs.io/en/stable/

jwt = JWTManager(app)
jwt.init_app(app)

# Bluprints
# https://flask.palletsprojects.com/es/main/blueprints/

app.register_blueprint(userBlueprint)
app.register_blueprint(productBlueprint)

if __name__ == "__main__":
    app.run()