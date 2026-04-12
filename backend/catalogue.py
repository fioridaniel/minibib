from pathlib import Path

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
                return 'no matches for this query'
            return item

        elif isinstance(arg, str):
            res = [
                (item_number, arg) 
                for item_number, details in self.inventory.items() 
                if details.get("topic") == arg
            ]

            return res if res else 'no matches for this query'
    
    # atualiza o inventário atual de um item adicionando a quantidade especificada (positiva ou negativa).
    def update(self, item_number, qty): 
        if item_number not in self.inventory:
            return 'iventario inexistente'
        
        self.inventory[item_number]["stock"] += qty
        return 'iventario atualizado com sucesso'