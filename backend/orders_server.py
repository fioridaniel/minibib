import grpc
import sys
import os
from concurrent import futures

# Adiciona path para proto
proto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'proto')
sys.path.insert(0, proto_path)

import bookstore_pb2
import bookstore_pb2_grpc

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
        
        # Verifica se o item existe e tem estoque
        qry_res = self.catalogue_stub.Query(
            bookstore_pb2.QueryRequest(arg=str(item_number))
        )
        
        if not qry_res.success:
            return bookstore_pb2.OrderResponse(
                success = False,
                error = 'item not found' 
            )
        
        # Verifica se há estoque disponível
        if qry_res.stock <= 0:
            return bookstore_pb2.OrderResponse(
                success = False,
                error = 'out of stock'
            )
        
        # Decrementa o estoque em 1
        update_res = self.catalogue_stub.Update(
            bookstore_pb2.UpdateRequest(item_number=item_number, qty=-1)
        )
        
        if not update_res.success:
            return bookstore_pb2.OrderResponse(
                success = False,
                error = 'failed to update inventory'
            )
        
        return bookstore_pb2.OrderResponse(
            success = True
        )


def main():
    if len(sys.argv) < 3:
        print("Uso: python orders_server.py <porta> <catalogue_host:porta>")
        print("Exemplo: python orders_server.py 50052 localhost:50051")
        sys.exit(1)
    
    port = sys.argv[1]
    catalogue_host = sys.argv[2]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_OrdersServiceServicer_to_server(
        OrdersServer(catalogue_host), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    print(f"Servidor de Pedidos rodando na porta {port}...")
    print(f"Conectado ao Catalogo em {catalogue_host}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()