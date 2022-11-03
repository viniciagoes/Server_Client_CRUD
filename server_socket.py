'''
    Vinicius e Gianluca
    Trabalho de Sistemas Distribuídos - Comunicação cliente servidor por socket
'''
import socket
import os

host = "localhost" 
port = 6030
BUFFER_SIZE = 1024  

'''
    Using the "with" operator, an instance of the socket type object is created,
    which will be destroyed after the execution of the indented section below,
    making it unnecessary to use socket_close().
'''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:

    socket_tcp.bind((host, port))
    socket_tcp.listen(5)  
    connection, address = socket_tcp.accept()  
    current_key = int(0)
    storage = {}

    with connection:
        print(f'Connection Established with machine {host} at port {port}.') 
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                break
            else:
                print('Data received: {}'.format(data.decode('UTF-8')))

                # Create
                if data.decode('UTF-8') == "1":
                    list_of_items = []
                    
                    new_item = connection.recv(BUFFER_SIZE)
                    new_item = new_item.decode('UTF-8')
                    print("New item received.")

                    quantity = connection.recv(BUFFER_SIZE)
                    quantity = quantity.decode('UTF-8')
                    print("New item quantity logged.")
                    
                    list_of_items.append(new_item)
                    list_of_items.append(quantity)
                    storage[current_key] = list_of_items
                    print(storage)

                    connection.send(bytes("Item added succesfully at", 'UTF-8'))
                    connection.send(bytes(str(current_key), 'UTF-8'))
                    current_key += 1

                # Read - when it sends None, there is no ID
                if data.decode('UTF-8') == "2":
                    id_of_interest = connection.recv(BUFFER_SIZE)

                    if storage.get(int(id_of_interest)) == None:
                        print('Item ID not found.')
                        item = '-1'
                        quantity = '-1'
                    else:
                        obj_stored = storage[int(id_of_interest)]
                        item = obj_stored[0]
                        quantity = obj_stored[1]
                        print(f'Found in stock: {item}, {quantity} units.')

                    connection.send(item.encode("UTF-8"))
                    connection.send(quantity.encode('UTF-8'))

                # Update
                if data.decode('UTF-8') == "3":
                    id_of_interest = connection.recv(BUFFER_SIZE)
                    quantity_updated = connection.recv(BUFFER_SIZE)
                    item_updated = connection.recv(BUFFER_SIZE)
                    
                    print(f'Updating item ID {id_of_interest}.')

                    item_updated = item_updated.decode("UTF-8")
                    print(f'New item name: {item_updated}')
                    
                    quantity_updated = quantity_updated.decode("UTF-8")
                    print(f'New item quantity: {quantity_updated}')

                    if storage.get(int(id_of_interest)) == None:
                        print('Item ID not found.')
                        item = '-1'
                        quantity = '-1'
                        connection.send(item.encode("UTF-8"))
                        connection.send(quantity.encode('UTF-8'))
                        
                    else:
                        obj_stored = storage[int(id_of_interest)]
                        item = obj_stored[0]
                        quantity = obj_stored[1]
                        print(f'Found in stock: {item}, {quantity} units.')

                        obj_stored[0] = item_updated
                        obj_stored[1] = quantity_updated

                        connection.send(obj_stored[0].encode("UTF-8"))
                        connection.send(obj_stored[1].encode('UTF-8'))

                # Delete
                if data.decode('UTF-8') == "4":
                    id_of_interest = connection.recv(BUFFER_SIZE)

                    if storage.get(int(id_of_interest)) == None:
                        error = '-1'
                        connection.send(error.encode("UTF-8"))
                        connection.send(bytes(id_of_interest))
                    else:
                        temp = int(id_of_interest)
                        del storage[temp]
                        print(storage)
                        print('Item succesfully deleted.')
                        connection.send(bytes("Item removed succesfully at ", 'UTF-8'))
                        connection.send(bytes(str(temp), 'UTF-8'))

                # Exit
                if data.decode('UTF-8') == "5":
                    os.system('cls')
                    break