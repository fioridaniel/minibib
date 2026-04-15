class Catalogue:
    def __init__(self):
        self.inventory = {
            793: {"name": "Socket Programming for Dummies", "topic": "sistemas", "stock": 25},
            794: {"name": "Python Crash Course", "topic": "sistemas", "stock": 10},
            795: {"name": "The Alchemist", "topic": "romance", "stock": 5},
        }

    # consulta detalhes do inventário atual (por tópico ou por número do item).
    def query(self, arg):
        if isinstance(arg, int):
            if not (item := self.inventory.get(arg)):
                return None
            return item

        elif isinstance(arg, str):
            res = [
                item_number
                for item_number, details in self.inventory.items() 
                if details.get("topic") == arg
            ]

            return res if res else None
    
    # atualiza o inventário atual de um item adicionando a quantidade especificada (positiva ou negativa).
    def update(self, item_number, qty): 
        if item_number not in self.inventory:
            return False
        
        curr_stock = self.inventory[item_number]["stock"]
        
        self.inventory[item_number]["stock"] = max(curr_stock + qty, 0)

        return True
    
    # retorna todos os livros do catálogo
    def list_all(self):
        return self.inventory