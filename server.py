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
            option = client.recv(1024).decode('utf8')
        except:
            break
        if not option:
            break

        match option:
            case "LOGIN":
                print("Logging in")

                client_name = client.recv(1024).decode('utf8')
                client.sendall(client_name.encode('utf8'))

                client_psw = client.recv(1024).decode('utf8')
                client.sendall(client_psw.encode('utf8'))

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
                
                if not loggedIn:
                    print("Logging in failed")
                break
            case "SIGNUP":
                print("Signing up")

                client_name = client.recv(1024).decode('utf8')
                client.sendall(client_name.encode('utf8'))

                client_psw = client.recv(1024).decode('utf8')
                client.sendall(client_psw.encode('utf8'))

                f = open('accounts.json', 'r+')
                file_data = json.load(f)

                for i in file_data['username']:
                    if i == client_name:
                        print('Username existed')
                        f.close()
                        return

                # Append new user's account to database
                file_data['username'].append(client_name)
                file_data['password'].append(client_psw)

                f.seek(0)
                json.dump(file_data, f, indent=4)

                print("Create account succesfully")
                f.close()

                print(client_name)
                print(client_psw)


            
    print("Disconnected")
    client.close()



        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()