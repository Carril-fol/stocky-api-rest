from repositories.repository import Repository
from entities.category_entity import CategoryEntity

class CategoryRepository(Repository):

    def get_category_by_id(self, id: int):
        with self.get_session() as session:
            return session.query(CategoryEntity).filter(CategoryEntity.id == id).first()
        
    def get_categories(self):
        with self.get_session() as session:
            return session.query(CategoryEntity).all()

    def create_category(self, category: CategoryEntity):
        with self.get_session() as session:
            session.add(category)
            session.commit()
            session.refresh(category)
            return category
    
    def update_category(self, category: CategoryEntity):
        with self.get_session() as session:
            merged_category = session.merge(category)
            session.commit()
            session.refresh(merged_category)
            return merged_category
        
    def delete_category(self, category: CategoryEntity):
        with self.get_session() as session:
            merged_category = session.merge(category)
            session.commit()
            session.refresh(merged_category)
            return merged_category