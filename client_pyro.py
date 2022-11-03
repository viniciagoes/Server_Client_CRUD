import sys
import Pyro4

# Exibir o menu principal (clientside)
def prompt():
    print("Stock management:")
    print("1 - Create")
    print("2 - Read")
    print("3 - Update")
    print("4 - Delete")
    print("5 - Exit")

    control = input(":")
    return control

storage = Pyro4.Proxy("PYRONAME:gianlucavinicius")
input("storage = Pyro4.Proxy(""PYRONAME:gianlucavinicius"") | Pressione uma tecla para continuar")


try:
    storage._pyroBind()
    input("storage._pyroBind() | Pressione uma tecla para continuar")
except:
    print("Error connecting")
    sys.exit(1)

# Variável utilizada para escolha das operações
control = 0

item = ""

while (control != '5'): # control == 5 sai do menu e encerra o programa
    control = prompt()

    # Operação Create (clientside)
    if control == '1':
        name = input("\nType name to create: ")
        quantity = int(input("Type quantity of item: "))

        item = storage.create(name, quantity)

        if item != 1:
            print(f"\nItem created sucessfully! ID:{item-1}\n")
        else:
            print("\nError creating item\n")

    # Operação Read (clientside)
    elif control == '2':
        id = int(input("\nType ID to read: "))
        item = storage.read(id)

        if item != None:
            for i in item:
                print("\nID: {0}\nName: {1}\nQuantity: {2}\n".format(i["id"], i["name"], i["quantity"]))
        else:
            print("\nError, ID unreachable\n")

    # Operação Update (clientside)
    elif control == '3':
        id = int(input("\nType ID to update: "))

        item = storage.read(id)

        if item != None:
            for i in item:
                print("\nItem being updated:\nID: {0}\nName: {1}\nQuantity: {2}\n".format(i["id"], i["name"], i["quantity"]))
            
            newname = input("\nType new item name: ")
            newquantity = int(input("Type new item quantity: "))
            item = storage.updateS(id, newname, newquantity)

            if item == id:
                print(f"\nItem updated sucessfully!\n")
            else:
                print("\nError updating item\n")
        else:
            print("\nError, ID unreachable\n")

    # Operação Delete (clientside)
    elif control == '4':
        id = int(input("\nType ID to delete: "))

        item = storage.read(id)

        if item != None:
            for i in item:
                print("\nItem being deleted:\nID: {0}\nName: {1}\nQuantity: {2}\n".format(i["id"], i["name"], i["quantity"]))
                
            item = storage.delete(id)

            if item == id:
                print("\nItem deleted succesfully!\n")
            else:
                print("\nError deleting item")
        else:
            print("\nError, ID unreachable\n")
