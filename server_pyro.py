import Pyro4

# Classe Item armazena as informações de cada objeto manipulado
class Item:
    name = ""
    quantity = 0
    id = 0

    # Cada objeto Item possui um nome, uma quantidade e um identificador
    def __init__(self, id:int, name:str, quantity:int):
        self.name = name
        self.quantity = quantity
        self.id = id

    def update(self, name:str, quantity:int):
        self.name = name
        self.quantity = quantity

# Comando expose torna visíveis/acessíveis os métodos descritos abaixo
@Pyro4.expose
class Storage():
    storage = []
    id = 1

    # Operação Create (serverside)
    def create(self, name:str, quantity:int):
        item =  Item(self.id, name, quantity)
        self.id += 1
        self.storage.append(item)
        
        return self.id

    # Operação Read (serverside)
    def read(self, id:int): 
        returnList = []

        if len(self.storage) > 0 and len(self.storage) >= id:
            item = [i for i in self.storage if i.id == id]

            i = list(item)[0]
            returnItem = {
                "id": id,
                "name": i.name,
                "quantity": i.quantity,
            }
            returnList.append(returnItem)
            return returnList
            
        else:
            return None

    # Operação Update (serverside)
    def updateS(self, id:int, newname:str, newquantity:str):
        item = [i for i in self.storage if i.id == id]

        if len(item) > 0 and item[0] != None:
            item[0].update(newname, newquantity)
            sucess = True
        if sucess:
            return id
        else:
            return None

    # Operação Delete (serverside)
    def delete(self, id:int):
        item = [i for i in self.storage if i.id == id]

        if len(item) > 0 and item[0] != None:
            try:
                self.storage.remove(item[0])
                sucess = True
            except:
                sucess = False
        if sucess:
            return id
        else:
            return None

# Na main, criamos o daemon do Pyro, registramos e iniciamos nosso serviço
def main():
    storage = Storage()
    input("storage = Storage() | Pressione uma tecla para continuar")

    daemon = Pyro4.Daemon()
    input("daemon = Pyro4.Daemon | Pressione uma tecla para continuar")

    endereco = daemon.register(storage)
    input("endereco = daemon.register(storage) | Pressione uma tecla para continuar")

    print("Endereço: ", endereco)

    servico = Pyro4.locateNS()
    input("Pyro4.locateNS() | Pressione uma tecla para continuar")

    servico.register("gianlucavinicius",endereco)
    input("servico.register(""storage"",endereco) | Pressione uma tecla para continuar")


    daemon.requestLoop()

if __name__ == "__main__":
    main()