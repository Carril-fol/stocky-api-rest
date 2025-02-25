from sqlalchemy.exc import SQLAlchemyError

from .service import BaseService
from repositories.repository import Repository

class CoreService(BaseService):

    def __init__(self):
        self._repository = Repository()

    def check_status_database(self):
        try:
            self._repository.check_database()
            return True
        except SQLAlchemyError:
            return False