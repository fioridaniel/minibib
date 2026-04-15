import grpc
import sys
import os

# Adiciona path para proto
proto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'proto')
sys.path.insert(0, proto_path)

import bookstore_pb2
import bookstore_pb2_grpc


class MinibibClient:
    def __init__(self, frontend_host):
        """
        Inicia o cliente e conecta ao servidor front-end.
        """
        channel = grpc.insecure_channel(frontend_host)
        self.frontend_stub = bookstore_pb2_grpc.FrontendServiceStub(channel)

    def search(self, topic):
        """
        Busca todos os itens de um tópico específico.
        """
        try:
            res = self.frontend_stub.Search(
                bookstore_pb2.SearchRequest(topic=topic)
            )
            
            if not res.success:
                print(f"Erro: {res.error}")
                return
            
            if not res.item_numbers:
                print(f"Nenhum livro encontrado para o tópico '{topic}'")
                return
            
            print(f"Livros encontrados para '{topic}':")
            for item_num in res.item_numbers:
                print(f"   - Item #{item_num}")
        
        except grpc.RpcError as e:
            print(f"Erro de comunicacao: {e.details()}")

    def lookup(self, item_number):
        """
        Consulta os detalhes de um item específico.
        """
        try:
            res = self.frontend_stub.Lookup(
                bookstore_pb2.LookupRequest(item_number=item_number)
            )
            
            if not res.success:
                print(f"Erro: {res.error}")
                return
            
            print(f"\nDetalhes do Livro #{item_number}:")
            print(f"   Nome: {res.name}")
            print(f"   Topico: {res.topic}")
            print(f"   Em estoque: {res.stock} copias\n")
        
        except grpc.RpcError as e:
            print(f"Erro de comunicacao: {e.details()}")

    def buy(self, item_number):
        """
        Compra um livro (decrementando o estoque em 1).
        """
        try:
            res = self.frontend_stub.Buy(
                bookstore_pb2.BuyRequest(item_number=item_number)
            )
            
            if not res.success:
                print(f"Compra falhou: {res.error}")
                return
            
            print(f"Livro #{item_number} comprado com sucesso!")
        
        except grpc.RpcError as e:
            print(f"Erro de comunicacao: {e.details()}")

    def list_all(self):
        """
        Lista todos os livros disponáveis no catálogo.
        """
        try:
            res = self.frontend_stub.ListAll(
                bookstore_pb2.ListAllRequest()
            )
            
            if not res.success:
                print(f"Erro: {res.error}")
                return
            
            if not res.books:
                print("Nenhum livro disponivel")
                return
            
            print("\n" + "="*70)
            print("CATALOGO COMPLETO DE LIVROS")
            print("="*70)
            print(f"{'ID':<6} {'Nome':<35} {'Topico':<12} {'Estoque':<6}")
            print("-"*70)
            
            for book in res.books:
                estoque_str = f"{book.stock}" if book.stock > 0 else "[Fora de estoque]"
                print(f"{book.item_number:<6} {book.name:<35} {book.topic:<12} {estoque_str:<6}")
            
            print("="*70 + "\n")
        
        except grpc.RpcError as e:
            print(f"Erro de comunicacao: {e.details()}")

    def interactive_menu(self):
        """
        Menu interativo para o cliente.
        """
        print("\n" + "="*50)
        print("MINIBIB.COM - Sistema de Livraria")
        print("="*50)
        
        while True:
            print("\nMenu:")
            print("1. Buscar livros por topico (search)")
            print("2. Ver detalhes de um livro (lookup)")
            print("3. Comprar um livro (buy)")
            print("4. Listar todos os livros (list)")
            print("5. Sair")
            
            choice = input("\nEscolha uma opcao (1-5): ").strip()
            
            if choice == "1":
                topic = input("Digite o topico: ").strip()
                if topic:
                    self.search(topic)
            
            elif choice == "2":
                try:
                    item_num = int(input("Digite o numero do item: ").strip())
                    self.lookup(item_num)
                except ValueError:
                    print("Digite um numero valido!")
            
            elif choice == "3":
                try:
                    item_num = int(input("Digite o numero do item a comprar: ").strip())
                    self.buy(item_num)
                except ValueError:
                    print("Digite um numero valido!")
            
            elif choice == "4":
                self.list_all()
            
            elif choice == "5":
                print("\nAte logo!")
                break
            
            else:
                print("Opcao invalida! Tente novamente.")


def main():
    if len(sys.argv) < 2:
        print("Uso: python client.py <frontend_host:porta>")
        print("Exemplo: python client.py localhost:50050")
        sys.exit(1)
    
    frontend_host = sys.argv[1]
    
    try:
        client = MinibibClient(frontend_host)
        client.interactive_menu()
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
