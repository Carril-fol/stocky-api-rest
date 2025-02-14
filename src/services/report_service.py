from .service import BaseService

from .stock_service import StockService

class ReportService(BaseService):

    def __init__(self):
        self.stock_service = StockService()

    def stock_report_excel(self):
        data = self.stock_service.stock_repository.get_stock_detailed_all()
        print(data)