import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SERVER_HOST = os.getenv("SERVER_HOST")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 1800
    JWT_REFRESH_TOKEN_EXPIRES = 2592000
    CORS_SUPPORTS_CREDENTIALS = True


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_HTTPONLY = True
    JWT_CSRF_IN_COOKIES = False
    JWT_COOKIE_SECURE = False 
    JWT_COOKIE_SAMESITE = "Lax"


class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_HTTPONLY = True
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = "None"

type_server = os.getenv("FLASK_ENV")

settings_from_server = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}