from modules.repository import Repository
from .user_entity import UserEntity

class UserRepository(Repository):

    def create_user(self, user: UserEntity, session=None):
        return self.create_register_entity(user, session=session)

    def update_user(self, user: UserEntity):
        return self.update_register_entity(user)
        
    def delete_user(self, user: UserEntity):
        return self.delete_register_entity(user)

    def get_user_by_id(self, id: int):
        with self.get_session() as session:
            user = session.query(UserEntity).filter(UserEntity.id == id).first()
            return user
        
    def get_user_by_email(self, email: str):
        with self.get_session() as session:
            user = session.query(UserEntity).filter(UserEntity.email == email).first()
            return user