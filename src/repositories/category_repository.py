from repositories.repository import Repository
from entities.category_entity import CategoryEntity

class CategoryRepository(Repository):

    def get_category_by_id(self, id: int) -> CategoryEntity:
        return self.get_register_entity(CategoryEntity, id)
        
    def get_categories(self) -> list[CategoryEntity]:
        return self.get_registers_entity(CategoryEntity)

    def create_category(self, category: CategoryEntity) -> CategoryEntity:
        return self.create_register_entity(category)
    
    def update_category(self, category: CategoryEntity) -> CategoryEntity:
        return self.update_register_entity(category)

    def delete_category(self, category: CategoryEntity) -> CategoryEntity:
        return self.delete_logic_register_entity(category)
    
    def get_category_by_name(self, name: str) -> CategoryEntity | None:
        with self.get_session() as session:
            return session.query(CategoryEntity).filter(CategoryEntity.name == name).first()
        