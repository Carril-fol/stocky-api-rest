from modules.repository import Repository
from modules.categories.category_entity import CategoryEntity

class CategoryRepository(Repository):

    def get_category_by_id(self, id: int, company_id: int = None) -> CategoryEntity | None:
        with self.get_session() as session:
            query = session.query(CategoryEntity).filter(CategoryEntity.id == id)

            if company_id is not None:
                query = query.filter(CategoryEntity.company_id == company_id)

            return query.first()
        
    def get_categories_by_company_id(
        self,
        company_id: int,
        page: int = 1,
        per_page: int = 10,
        search: str = None
    ):
        with self.get_session() as session:
            query = session.query(CategoryEntity)\
                .filter(CategoryEntity.company_id == company_id)

            if search:
                query = query.filter(CategoryEntity.name.ilike(f"%{search}%"))

            total = query.count()

            categories = query\
                .offset((page - 1) * per_page)\
                .limit(per_page)\
                .all()

            return categories, total

    def create_category(self, category: CategoryEntity) -> CategoryEntity:
        return self.create_register_entity(category)
    
    def update_category(self, category: CategoryEntity) -> CategoryEntity:
        return self.update_register_entity(category)

    def delete_category(self, category: CategoryEntity) -> CategoryEntity:
        return self.delete_logic_register_entity(category)
    
    def get_category_by_name(self, name: str, company_id: int) -> CategoryEntity | None:
        with self.get_session() as session:
            return session.query(CategoryEntity).filter(CategoryEntity.name == name, CategoryEntity.company_id == company_id).first()
        