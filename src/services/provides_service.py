from models.provides_model import ProvidesModel
from entities.provides_entity import ProvidesEntity
from repositories.provides_repository import ProviderRepository

class ProvidesService:

    def __init__(self):
        self._provider_repository = ProviderRepository()
        self._provides_model = ProvidesModel()

    def _prepare_provides_entity(self, data: dict, provider: ProvidesEntity = None):
        validated_data = self._provides_model.model_validate(data)
        if provider:
            for key, value in data.items():
                setattr(provider, key, value)
            return provider
        return validated_data

    def _provider_exists(self, id: int):
        provider = self._provider_repository.get_provider_by_id(id)
        if not provider:
            raise Exception('Register from that providers not found.')
        return provider
    
    def get_provider_by_id(self, id: int):
        provider = self._provider_exists(id)
        provider_dump = self._provides_model.model_validate(provider.__dict__).model_dump(by_alias=True)
        return provider_dump

    def create_provider(self, data: dict):
        provider_data_validated = self._prepare_provides_entity(data)
        provider_entity = ProvidesEntity(**provider_data_validated.model_dump())
        return self._provider_repository.create_provider(provider_entity)

    def update_provider(self, id: int, data: dict):
        provider = self._provider_exists(id)
        provider_to_update = self._prepare_provides_entity(data, provider)
        return self._provider_repository.update_provider(provider_to_update)