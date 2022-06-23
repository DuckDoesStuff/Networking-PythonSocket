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

        if option == "LOGIN":
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

            j = 0
            loggedIn = False
            for i in file_data['username']:
                if i == client_name:
                    if file_data['password'][j] == client_psw:
                        print("Login succesfully")
                        loggedIn = True
                        break
                    print("Wrong password")
                    break
                j += 1

            msg = ""
            if not loggedIn:
                msg = "Incorrect username or password"
                client.sendall(msg.encode(FORMAT))
                print("Logging in failed")
            else:
                msg = "LOGGEDIN"
                client.sendall(msg.encode(FORMAT))
                print("Logging in successful") 

        elif option == "SIGNUP":
            print("Signing up")

            client_name = client.recv(1024).decode(FORMAT)
            client.sendall(client_name.encode(FORMAT))

            client_psw = client.recv(1024).decode(FORMAT)
            client.sendall(client_psw.encode(FORMAT))

            f = open('accounts.json', 'r+')
            file_data = json.load(f)
            msg = ""
            for i in file_data['username']:
                if i == client_name:
                    print('Username already exist')
                    f.close()
                    msg = "Username already exist"
                    client.sendall(msg.encode(FORMAT))
                    return

            # Append new user's account to database
            file_data['username'].append(client_name)
            file_data['password'].append(client_psw)

            f.seek(0)
            json.dump(file_data, f, indent=4)

            print("Create account succesfully")
            f.close()

            msg = "SIGNEDUP"
            client.sendall(msg.encode(FORMAT))

            print(client_name)
            print(client_psw)

        
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