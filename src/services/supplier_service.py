from models.supplier_model import SupplierModel
from entities.supplier_entity import SupplierEntity
from repositories.supplier_repository import SupplierRepository

class SupplierService:
    
    def __init__(self):
        self._supplier_repository = SupplierRepository()
        self._supplier_model = SupplierModel()

    def _format_data_into_supplier_exists(self, data: dict, supplier: SupplierEntity):
        for key, value in data.items():
            setattr(supplier, key, value)
        return supplier

    def _format_data_into_model(self, data: dict):
        return self._supplier_model.model_validate(data)
    
    def _supplier_exists_by_name(self, supplier_model: SupplierModel):
        return self._supplier_repository.get_supplier_by_name(supplier_model.name) is not None  

    def create_supplier(self, data: dict):
        validated_data = self._format_data_into_model(data)
        if self._supplier_exists_by_name(validated_data):
            raise Exception('Supplier with that name already exists.')
        supplier = SupplierEntity(**validated_data.model_dump())
        return self._supplier_repository.create_supplier(supplier)

    def get_supplier_by_id(self, id: int):
        supplier = self._supplier_repository.get_suppliers_by_id(id)
        if not supplier:
            raise Exception('Supplier not found.')
        return supplier

    def update_supplier(self, id: int, data: dict):
        supplier = self._supplier_repository.get_suppliers_by_id(id)
        if not supplier:
            raise Exception('Supplier not found.')
        validated_data = self._format_data_into_model(data)
        if supplier.status == validated_data.status:
            raise Exception(f'Status from the supplier is already {supplier.status}.')
        supplier_data_updated = self._format_data_into_supplier_exists(data, supplier)
        return self._supplier_repository.update_supplier(supplier_data_updated)

    def delete_supplier(self, id: int):
        supplier = self._supplier_repository.get_suppliers_by_id(id)
        if not supplier:
            raise Exception('Supplier not found.')
        data = {'status': 'inactive'}
        validated_data = self._format_data_into_model(data)
        if supplier.status == validated_data.status:
            raise Exception(f'Status from the supplier is already {supplier.status}.')
        supplier_to_delete = self._format_data_into_supplier_exists(data, supplier)
        return self._supplier_repository.delete_supplier(supplier_to_delete)

    def get_suppliers(self):
        suppliers = self._supplier_repository.get_suppliers()
        for supplier in suppliers:
            validated_supplier = self._supplier_model.model_validate(supplier.__dict__).model_dump(by_alias=True)
            yield validated_supplier