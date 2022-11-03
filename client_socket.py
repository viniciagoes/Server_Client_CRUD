'''
    Vinicius e Gianluca
    Trabalho de Sistemas Distribuídos - Comunicação cliente servidor por socket
'''
import os
from socket import socket

BUFFER_SIZE = 1024 

def prompt():
    print("Stock management:")
    print("1 - Create")
    print("2 - Read")
    print("3 - Update")
    print("4 - Delete")
    print("5 - Exit")

def main():
    connection = socket()
    connection.connect(("localhost", 6030))
    control = 2  

    while control == 2:
        while True:
            prompt()
            option = input("Select an operation: ")
            connection.send(bytes(option, "UTF-8"))

            # Create
            if option == "1":
                output_data = input("Enter item name and quantity (separated by space): ")
                item, quantity = output_data.split()

                connection.send(bytes(item, "UTF-8"))
                connection.send(bytes(quantity, "UTF-8"))
                
                serv_return = connection.recv(BUFFER_SIZE)
                serv_return = serv_return.decode('UTF-8')
                key = connection.recv(BUFFER_SIZE)
                key = key.decode('UTF-8')
                print(f'[*] Server: {serv_return} ID {key}.\n')

            # Read
            elif option == "2":
                id_of_interest = input("Enter item ID to be displayed: ")
                connection.send(bytes(id_of_interest, "UTF-8"))
                
                item = connection.recv(BUFFER_SIZE)
                item = item.decode('UTF-8')
                quantity = connection.recv(BUFFER_SIZE)
                quantity = quantity.decode('UTF-8')
                
                if item != '-1':
                    print(f'[*] Server: Found in stock: {item}, {quantity} units.\n')
                else:
                    print("[*] Server: Item ID not found.\n")
                    break

            # Update
            elif option == "3":
                id_of_interest = input("Enter item ID to be updated: ")
                
                output_data = input("Enter new item name and quantity (separated by space): ")
                item, quantity = output_data.split()

                connection.send(bytes(id_of_interest, "UTF-8"))
                connection.send(bytes(item, "UTF-8"))
                connection.send(bytes(quantity, "UTF-8"))
                
                item = connection.recv(BUFFER_SIZE)
                item = item.decode('UTF-8')
                quantity = connection.recv(BUFFER_SIZE)
                quantity = quantity.decode('UTF-8')

                if item != '-1':
                    print(f'[*] Server: Item updated: {item}, {quantity} units.\n')
                else:
                    print("[*] Server: Item ID not found.\n")


            # Delete
            elif option == "4":
                id_of_interest = input("Enter item ID to be deleted: ")
                connection.send(bytes(id_of_interest, "UTF-8"))

                serv_return = connection.recv(BUFFER_SIZE)
                serv_return = serv_return.decode('UTF-8')
                key = connection.recv(BUFFER_SIZE)
                key = key.decode('UTF-8')

                if serv_return == '-1':
                    print("[*] Server: Item ID not found.\n")
                else:
                    print(f'[*] Server: {serv_return}ID {key}.\n')
        
                
            # Exit
            elif option == "5":
                os.system('cls')
                control = 3
                break

            else:
                print("[*] Server: Invalid selection. Shutting down connection.\n")
                break

if __name__ == "__main__":
    main()