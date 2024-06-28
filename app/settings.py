import os
from dotenv import load_dotenv
load_dotenv()

# Flask
# https://flask.palletsprojects.com/en/3.0.x/

SECRET_KEY = os.environ.get("SECRET_KEY")

# PyMongo
# https://pymongo.readthedocs.io/en/stable/

MONGO_URI = os.environ.get("MONGO_URI")

# Flask JWTManager

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_TOKEN_LOCATION = ["headers"]
JWT_COOKIE_SECURE = False