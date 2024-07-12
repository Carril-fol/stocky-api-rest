from flask_restful import Resource

class HomeResource(Resource):
    """
    Example:

    GET: /
    ```
    Successful response (code 200 - OK):
    {
        "status": "API REST running"
    }
    ```
    """
    def get(self):
        return {"status": "API REST running"}, 200
    