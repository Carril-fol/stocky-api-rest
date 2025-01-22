from pydantic import BaseModel

class BaseService:

    def _prepare_to_entity(self, data: dict, model: BaseModel = None, instance_entity = None):
        validated_data = model.model_validate(data)
        if instance_entity:
            for key, value in data.items():
                setattr(instance_entity, key, value)
            return instance_entity
        return validated_data

    def _validate_and_serialize(self, entity, model: BaseModel):
        return model.model_validate(entity.__dict__).model_dump(by_alias=True)