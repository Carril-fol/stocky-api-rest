from flask import Flask
from flask_jwt_extended import JWTManager

from .users.controllers.user_controllers import user_blueprint
from .categories.controllers.category_controllers import category_blueprint

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
app.register_blueprint(user_blueprint)
app.register_blueprint(category_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
