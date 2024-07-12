import cherrypy
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from settings import PORT
from auth.controllers.user_controllers import *
from categories.controllers.category_controllers import *
from products.controllers.products_controllers import *
from products.controllers.products_details_controllers import *

# Flask
# https://flask.palletsprojects.com/en/3.0.x/
app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Flask-JWT-Extended
# https://flask-jwt-extended.readthedocs.io/en/stable/
jwt = JWTManager(app)
jwt.init_app(app)

# Flask-Restful
# https://flask-restful.readthedocs.io/en/latest/index.html
api = Api(app)

api.add_resource(UserRegisterResource, "/users/api/v1/register")
api.add_resource(UserLoginResource, "/users/api/v1/login")
api.add_resource(UserLogoutResource, "/users/api/v1/logout")
api.add_resource(UserDetailsResource, "/users/api/v1/<user_id>")

api.add_resource(ProductCreateResource, "/product/api/v1/create")
api.add_resource(ProductDeleteResource, "/product/api/v1/delete/<product_id>")
api.add_resource(ProductDetailByIdResource, "/product/api/v1/detail/<product_id>")
api.add_resource(ProductUpdateResource, "/product/api/v1/update/<product_id>")

api.add_resource(ProductDetailCreateResource, "/product/detail/api/v1/create")
api.add_resource(ProductDetailGetResource, "/product/detail/api/v1/<barcode>")
api.add_resource(ProductDetailDeleteResource, "/product/detail/api/v1/delete/<barcode>")

api.add_resource(CategoryCreateResource, "/categories/api/v1/create")
api.add_resource(CategoryDetailByNameResource, "/categories/api/v1/<name>")
api.add_resource(CategoryAllDetailResource, "/categories/api/v1/all")
api.add_resource(CategoryDeleteResource, "/categories/api/v1/delete/<category_id>")
api.add_resource(CategoryUpdateResource, "/categories/api/v1/update/<category_id>")

if __name__ == "__main__":
    cherrypy.tree.graft(app, "/")
    cherrypy.config.update({
        "server.socket_host": "0.0.0.0",
        "server.socket_port": int(PORT)
    })
    cherrypy.engine.start()
    cherrypy.engine.block()