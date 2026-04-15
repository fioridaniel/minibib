import grpc
import sys
import os
from concurrent import futures

# Adiciona path para proto
proto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'proto')
sys.path.insert(0, proto_path)

from catalogue import Catalogue
import bookstore_pb2
import bookstore_pb2_grpc as bookstore_pb2_grpc

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

    def ListAll(self, request, context):
        inventory = self.catalogue.list_all()
        books = []
        
        for item_number, details in inventory.items():
            book = bookstore_pb2.Book(
                item_number=item_number,
                name=details["name"],
                topic=details["topic"],
                stock=details["stock"]
            )
            books.append(book)
        
        return bookstore_pb2.ListAllResponse(
            success=True,
            books=books
        )


def main():
    if len(sys.argv) < 2:
        print("Uso: python catalogue_server.py <porta>")
        print("Exemplo: python catalogue_server.py 50051")
        sys.exit(1)
    
    port = sys.argv[1]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_CatalogueServiceServicer_to_server(
        CatalogueServer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    print(f"Servidor de Catalogo rodando na porta {port}...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()