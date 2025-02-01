from .service import BaseService
from models.supplier_model import SupplierModel
from entities.supplier_entity import SupplierEntity
from repositories.supplier_repository import SupplierRepository
from exceptions.supplier_exceptions import (
    SupplierNotFound,
    SupplierAlreadyExists,
    SupplierHasAlreadyStatus
)

class SupplierService(BaseService):
    
    def __init__(self):
        self._supplier_repository = SupplierRepository()
        self._supplier_model = SupplierModel()
    
    def _supplier_exists_by_name(self, supplier_model: SupplierModel):
        supplier = self._supplier_repository.get_supplier_by_name(supplier_model.name)
        if supplier:
            raise SupplierAlreadyExists()
        return supplier

    def _supplier_exists_by_id(self, id: int):
        supplier = self._supplier_repository.get_suppliers_by_id(id)
        if not supplier:
            raise SupplierNotFound()
        return supplier
    
    def _check_status_supplier(self, supplier: SupplierEntity, data: dict):
        if supplier.status == data.get('status'):
            raise SupplierHasAlreadyStatus()
        return supplier

    def create_supplier(self, data: dict):
        supplier_data_validated = self._prepare_to_entity(data, self._supplier_model)
        self._supplier_exists_by_name(supplier_data_validated)
        supplier = SupplierEntity(**supplier_data_validated.model_dump())
        return self._supplier_repository.create_supplier(supplier)

    def get_supplier_by_id(self, id: int):
        supplier = self._supplier_exists_by_id(id)
        return self._validate_entity_and_serialize(supplier, self._supplier_model)

    def update_supplier(self, id: int, data: dict):
        supplier = self._supplier_exists_by_id(id)
        self._check_status_supplier(supplier, data)
        supplier_to_update = self._prepare_to_entity(data, self._supplier_model, supplier)
        return self._supplier_repository.update_supplier(supplier_to_update)

    def delete_supplier(self, id: int, data: dict):
        supplier = self._supplier_exists_by_id(id)
        self._check_status_supplier(supplier, data)
        supplier_to_delete = self._prepare_to_entity(data, self._supplier_model, supplier)
        return self._supplier_repository.delete_supplier(supplier_to_delete)

    def get_suppliers(self):
        suppliers = self._supplier_repository.get_suppliers()
        for supplier in suppliers:
            validated_supplier = self._validate_entity_and_serialize(supplier, self._supplier_model)
            yield validated_supplier