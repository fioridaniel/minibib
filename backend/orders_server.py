import grpc

from proto import bookstore_pb2, bookstore_pb2_grpc

"""
    Verifica se o item está em estoque consultando o servidor de
    catálogo e, em seguida, decrementa o número de itens em estoque em um. O pedido pode
    falhar se o item estiver fora de estoque.
"""

class OrdersServer(bookstore_pb2_grpc.OrdersServiceServicer):
    def __init__(self, catalogue_host):
        # cria um canal gRPC para o catalogo
        channel = grpc.insecure_channel(catalogue_host)
        self.catalogue_stub = bookstore_pb2_grpc.CatalogueServiceStub(channel)

    def Buy(self, request, context):
        item_number = request.item_number
        
        qry_res = self.catalogue_stub.Query(
            bookstore_pb2.QueryRequest(arg=str(item_number))
        )
        
        if not qry_res.success:
            return bookstore_pb2.OrderResponse(
                success = False,
                error = 'no matches' 
            )
        
        update_req = item_number, -1 
        update_res = self.catalogue_stub.Update(
            bookstore_pb2.UpdateRequest(item_number=item_number, qty=-1)
        )
        
        if not update_res:
            return bookstore_pb2.OrderResponse(
                success = False,
                error = 'not available to buy'
            )
        
        return bookstore_pb2.OrderResponse(
            success = True
        )