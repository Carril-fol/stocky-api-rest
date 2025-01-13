import uvicorn
from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv

from database.db import Database
load_dotenv()

def start_server(app):
    db = Database()
    db.initialize()

    host = app.config.get("SERVER_HOST")
    port = app.config.get("SERVER_PORT")
    app_asgi = WsgiToAsgi(app)
    uvicorn.run(app_asgi, host=host, port=port)