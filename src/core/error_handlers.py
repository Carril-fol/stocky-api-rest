from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        return jsonify({"error": error.name, "detail": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unhandled_exception(error: Exception):
        app.logger.exception("Unhandled exception: %s", error)
        return jsonify({"error": "Internal server error"}), 500
