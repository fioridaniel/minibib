import grpc
import sys
import os
from concurrent import futures

# Adiciona path para proto
proto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'proto')
sys.path.insert(0, proto_path)

import bookstore_pb2
import bookstore_pb2_grpc


class FrontendServer(bookstore_pb2_grpc.FrontendServiceServicer):
    def __init__(self, catalogue_host, orders_host):
        # Conecta aos servidores de catálogo e pedidos
        catalogue_channel = grpc.insecure_channel(catalogue_host)
        orders_channel = grpc.insecure_channel(orders_host)
        
        self.catalogue_stub = bookstore_pb2_grpc.CatalogueServiceStub(catalogue_channel)
        self.orders_stub = bookstore_pb2_grpc.OrdersServiceStub(orders_channel)

    def Search(self, request, context):
        """
        Busca todos os números de itens de um tópico específico.
        Chama o servidor de catálogo.
        """
        topic = request.topic
        
        res = self.catalogue_stub.Query(
            bookstore_pb2.QueryRequest(arg=topic)
        )
        
        if not res.success:
            return bookstore_pb2.SearchResponse(
                success=False,
                error=res.error
            )
        
        return bookstore_pb2.SearchResponse(
            success=True,
            item_numbers=res.item_numbers
        )

    def Lookup(self, request, context):
        """
        Consulta detalhes de um item específico (nome, tópico, estoque).
        Chama o servidor de catálogo.
        """
        item_number = request.item_number
        
        res = self.catalogue_stub.Query(
            bookstore_pb2.QueryRequest(arg=str(item_number))
        )
        
        if not res.success:
            return bookstore_pb2.LookupResponse(
                success=False,
                error=res.error
            )
        
        return bookstore_pb2.LookupResponse(
            success=True,
            name=res.name,
            topic=res.topic,
            stock=res.stock
        )

    def Buy(self, request, context):
        """
        Compra um item (decrementando o estoque em 1).
        Chama o servidor de pedidos.
        """
        item_number = request.item_number
        
        res = self.orders_stub.Buy(
            bookstore_pb2.OrderRequest(item_number=item_number)
        )
        
        return bookstore_pb2.BuyResponse(
            success=res.success,
            error=res.error
        )

    def ListAll(self, request, context):
        """
        Lista todos os livros disponáveis.
        Chama o servidor de catálogo.
        """
        res = self.catalogue_stub.ListAll(
            bookstore_pb2.ListAllRequest()
        )
        
        if not res.success:
            return bookstore_pb2.ListAllResponse(
                success=False,
                error=res.error
            )
        
        return bookstore_pb2.ListAllResponse(
            success=True,
            books=res.books
        )


def main():
    if len(sys.argv) < 4:
        print("Uso: python frontend-server.py <porta> <catalogue_host:porta> <orders_host:porta>")
        print("Exemplo: python frontend-server.py 50050 localhost:50051 localhost:50052")
        sys.exit(1)
    
    port = sys.argv[1]
    catalogue_host = sys.argv[2]
    orders_host = sys.argv[3]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_FrontendServiceServicer_to_server(
        FrontendServer(catalogue_host, orders_host), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    print(f"Servidor Front-end rodando na porta {port}...")
    print(f"Conectado ao Catalogo em {catalogue_host}")
    print(f"Conectado ao Pedidos em {orders_host}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()