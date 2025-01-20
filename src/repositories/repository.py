from contextlib import contextmanager
from database.db import Database

class Repository:

    @contextmanager
    def get_session(self):
        session = Database.get_session()
        try:
            yield session
        finally:
            session.close()