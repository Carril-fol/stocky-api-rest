from repositories.repository import Repository
from entities.provides_entity import ProvidesEntity

class ProviderRepository(Repository):

    def get_provider_by_id(self, id: int):
        return self.get_register_entity(ProvidesEntity, id)

    def create_provider(self, provides: ProvidesEntity):
        return self.create_register_entity(provides)
        
    def update_provider(self, provides: ProvidesEntity):
        return self.update_register_entity(provides)