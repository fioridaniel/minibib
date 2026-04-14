from catalogue import Catalogue

catalogue = Catalogue()

"""
    Verifica se o item está em estoque consultando o servidor de
    catálogo e, em seguida, decrementa o número de itens em estoque em um. O pedido pode
    falhar se o item estiver fora de estoque.
"""
def buy(item_number):
    item = catalogue.inventory.get(item_number)

    if item:
        curr_stock = item["stock"]
        item["stock"] = max(0, curr_stock - 1)
    
    else:
        return 'no matches for this query'