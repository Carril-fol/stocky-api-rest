from .service import BaseService
from models.supplier_model import SupplierModel, CreateUpdateSupplierModel
from entities.supplier_entity import SupplierEntity
from repositories.supplier_repository import SupplierRepository
from exceptions.supplier_exceptions import SupplierNotFound, SupplierAlreadyExists, SupplierHasAlreadyStatus

class SupplierService(BaseService):
    
    def __init__(self, supplier_repository: SupplierRepository):
        self._supplier_repository = supplier_repository
    
    def _supplier_exists_by_name(self, supplier_model: SupplierModel) -> SupplierAlreadyExists | SupplierEntity:
        supplier = self._supplier_repository.get_supplier_by_name(supplier_model.name)
        if supplier:
            raise SupplierAlreadyExists()
        return supplier

    def _supplier_exists_by_id(self, id: int) -> SupplierNotFound | SupplierEntity:
        supplier = self._supplier_repository.get_suppliers_by_id(id)
        if not supplier:
            raise SupplierNotFound()
        return supplier
    
    def _check_status_supplier(self, supplier: SupplierEntity, data: dict) -> SupplierHasAlreadyStatus | SupplierEntity:
        if supplier.status == data.get('status'):
            raise SupplierHasAlreadyStatus()
        return supplier

    def create_supplier(self, data: dict) -> SupplierEntity:
        supplier_data_validated = CreateUpdateSupplierModel.model_validate(data)
        self._supplier_exists_by_name(supplier_data_validated)

        supplier = SupplierEntity(**supplier_data_validated.model_dump())
        return self._supplier_repository.create_supplier(supplier)

    def get_supplier_by_id(self, id: int) -> dict:
        supplier = self._supplier_exists_by_id(id)
        return SupplierModel.model_validate(supplier.to_dict()).model_dump(by_alias=True)
    
    def update_supplier(self, id: int, data: dict) -> SupplierEntity:
        supplier = self._supplier_exists_by_id(id)
        self._check_status_supplier(supplier, data)
        supplier_validated = CreateUpdateSupplierModel.model_validate(data).model_dump(by_alias=True, exclude_unset=True)

        supplier_to_update = self._update_instance_entity(supplier_validated, supplier)
        return self._supplier_repository.update_supplier(supplier_to_update)

    def delete_supplier(self, id: int, data: dict) -> SupplierEntity:
        supplier = self._supplier_exists_by_id(id)
        self._check_status_supplier(supplier, data)

        supplier_to_delete: SupplierEntity = self._update_instance_entity(data, supplier)
        return self._supplier_repository.delete_supplier(supplier_to_delete)

    def get_suppliers(self) -> list[dict]:
        suppliers = []
        for supplier in self._supplier_repository.get_suppliers():
            supplier_formated = SupplierModel.model_validate(supplier.to_dict()).model_dump(by_alias=True)
            suppliers.append(supplier_formated)
        return suppliers