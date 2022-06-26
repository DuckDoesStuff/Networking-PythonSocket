from logging import Logger
from socket import *
from threading import *
import json


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    while True:
        try:
            option = client.recv(1024).decode(FORMAT)
        except:
            break
        if not option:
            break
        print(option)
        if option == "SIGNIN":
            print("Logging in")

            client_name = client.recv(1024).decode(FORMAT)
            client.sendall(client_name.encode(FORMAT))

            client_psw = client.recv(1024).decode(FORMAT)
            client.sendall(client_psw.encode(FORMAT))

            print(client_name)
            print(client_psw)

            #Open and store loaded data as a python object
            f = open('accounts.json', 'r')
            file_data = json.load(f)
            f.close()
            
            loggedIn = False
            for user in file_data:
                if user['username'] == client_name:
                    if user['password'] == client_psw:
                        print("Login success")
                        client.sendall("SIGNEDIN".encode(FORMAT))
                        loggedIn = True
                    else:
                        print("Login failed")
                    break
            
            if not loggedIn:
                client.sendall("Incorrect username or password".encode(FORMAT))

        elif option == "SIGNUP":
            print("Signing up")

            client_name = client.recv(1024).decode(FORMAT)
            client.sendall(client_name.encode(FORMAT))

            client_psw = client.recv(1024).decode(FORMAT)
            client.sendall(client_psw.encode(FORMAT))

            print(client_name)
            print(client_psw)

            f = open('accounts.json', 'r+')
            file_data = json.load(f)
            
            existed = False
            for user in file_data:
                if user['username'] == client_name:
                    print('Username already exist')
                    f.close()
                    client.sendall("Username already exist".encode(FORMAT))
                    existed = True
                    break
            
            if not existed:
                # Append new user's account to database
                info = {
                    "username" : client_name,
                    "password" : client_psw
                }

                file_data.append(info)

                f.seek(0)
                json.dump(file_data, f, indent=4)

                print("Create account succesfully")
                f.close()

                client.sendall("SIGNEDUP".encode(FORMAT))

        
    print(str(addresses[client][0]) + ":" + str(addresses[client][1]) + " has disconnected")
    client.close()
        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()