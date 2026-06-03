from modules.service import BaseService

from .supplier_model import SupplierModel, CreateSupplierModel, UpdateSupplierModel
from .supplier_entity import SupplierEntity
from .supplier_repository import SupplierRepository
from .supplier_exceptions import SupplierNotFound, SupplierAlreadyExists, SupplierHasAlreadyStatus


class SupplierService(BaseService):
    
    def __init__(self, supplier_repository: SupplierRepository):
        self._supplier_repository = supplier_repository

    # --------------------------------------------------------
    # Private functions
    # --------------------------------------------------------

    def _supplier_exists_by_name(self, supplier_model, company_id: int = None) -> SupplierAlreadyExists | SupplierEntity:
        supplier = self._supplier_repository.get_supplier_by_name(supplier_model.name, company_id)
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

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------

    def create_default_supplier(self):
        data = { "name": "SIN PROVEEDOR", "status": "ACTIVE" }
        supplier_model_data = CreateSupplierModel.model_validate(data)

        if not self._supplier_repository.get_supplier_by_name(supplier_model_data.name):
            supplier_model_dump = supplier_model_data.model_dump()
            supplier_to_create = SupplierEntity(**supplier_model_dump)
            self._supplier_repository.create_supplier(supplier_to_create)

    def create_supplier(self, data: dict, company_id: int) -> SupplierEntity:
        supplier_data_validated = CreateSupplierModel.model_validate(data)
        self._supplier_exists_by_name(supplier_data_validated, company_id)

        supplier = SupplierEntity(**supplier_data_validated.model_dump())
        return self._supplier_repository.create_supplier(supplier)

    def get_supplier_by_id(self, id: int) -> dict:
        supplier = self._supplier_exists_by_id(id)
        return SupplierModel.model_validate(supplier.to_dict()).model_dump(by_alias=True)
    
    def update_supplier(self, id: int, data: dict, company_id: int) -> SupplierEntity:
        supplier = self._supplier_exists_by_id(id)
        self._check_status_supplier(supplier, data)
        

        supplier_validated = UpdateSupplierModel.model_validate(
            data,
            context={'company_id': company_id}
        ).model_dump(by_alias=True, exclude_unset=True)

        supplier_to_update = self._update_instance_entity(supplier_validated, supplier)
        return self._supplier_repository.update_supplier(supplier_to_update)

    def delete_supplier(self, id: int, data: dict) -> SupplierEntity:
        supplier = self._supplier_exists_by_id(id)
        self._check_status_supplier(supplier, data)

        supplier_to_delete: SupplierEntity = self._update_instance_entity(data, supplier)
        return self._supplier_repository.delete_supplier(supplier_to_delete)

    def get_suppliers(self, company_id: int) -> list[dict]:
        suppliers = []
        for supplier in self._supplier_repository.get_suppliers(company_id):
            supplier_formated = SupplierModel.model_validate(supplier.to_dict()).model_dump(by_alias=True)
            suppliers.append(supplier_formated)
        return suppliers