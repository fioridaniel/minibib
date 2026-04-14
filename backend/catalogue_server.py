from catalogue import Catalogue
from proto import bookstore_pb2, bookstore_pb2_grpc

class CatalogueServer(bookstore_pb2_grpc.CatalogueServiceServicer):
    def __init__(self):
        self.catalogue = Catalogue()

    def Query(self, request, context):
        arg = request.arg
        
        try:
            arg = int(arg)  
        except ValueError:
            pass  

        res = self.catalogue.query(arg)

        if res is None:
            return bookstore_pb2.QueryResponse(success=False, error='no matches')

        if isinstance(res, list):
            return bookstore_pb2.QueryResponse(
                success = True,
                item_numbers = res
            )
        
        return bookstore_pb2.QueryResponse(
            success = True,
            name = res["name"],
            topic = res["topic"],
            stock = res["stock"]
        )

    def Update(self, request, context):
        item_number = request.item_number
        qty = request.qty

        res = self.catalogue.update(item_number, qty)

        if res:
            return bookstore_pb2.UpdateResponse(
                success = True
            )

        return bookstore_pb2.UpdateResponse(
            success = False,
            error = 'item not found'
        )