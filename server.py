from socket import *
from threading import *
import json
import os


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
            client.sendall(option.encode(FORMAT))

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
            client.recv(1024)

        elif option == "SIGNUP":
            print("Signing up")
            client.sendall(option.encode(FORMAT))

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

                newfolder = "./storage/" + client_name
                os.mkdir(newfolder)
                file = open("./storage/" + client_name + "/note.json", "w")
                temp_dict = [
                ]
                temp_string = json.dumps(temp_dict, sort_keys=True, indent=4)
                file.write(temp_string)
                file.close()
                
                file = open("./storage/" + client_name + "/file.json", "w")
                temp_dict = [
                ]
                temp_string = json.dumps(temp_dict, sort_keys=True, indent=4)
                file.write(temp_string)
                file.close()

                file = open("./storage/" + client_name + "/image.json", "w")
                temp_dict = [
                ]
                temp_string = json.dumps(temp_dict, sort_keys=True, indent=4)
                file.write(temp_string)
                file.close()

                print("Create account succesfully")
                f.close()

                client.sendall("SIGNEDUP".encode(FORMAT))
            client.recv(1024)

        elif option == "UPLOAD":
            client.sendall(option.encode(FORMAT))

            file_type = client.recv(1024).decode(FORMAT)
            client.sendall(file_type.encode(FORMAT))

            filepath = client.recv(1024).decode(FORMAT)
            client.sendall(filepath.encode(FORMAT))

            os.path.split(filepath)
            filename = os.path.split(filepath)[1]

            cwd = os.getcwd()
            print(cwd)

            upld_path = "./storage/" + client_name
            if not os.path.exists(upld_path):
                os.mkdir(upld_path)
            os.chdir(upld_path)

            print(os.getcwd())

            file = open(filename, "wb")
            data = client.recv(2048)
            client.sendall(data)
            running = True
            while running:
                file.write(data)
                try:
                    data = client.recv(2048)
                    client.sendall(data)
                    if data.decode(FORMAT) == "DONE" or not data:
                        running = False
                except UnicodeDecodeError:
                    pass
            file.close()
            os.chdir(cwd)    
            print(filename)
            print("Receiving completed")
            
            # if file_type == "IMAGE":
            #     namestore = upld_path + '/image.json'
            # else: 
            namestore = upld_path + '/file.json'
            storage = open(namestore, 'r+')
            file_data = json.load(storage)

            info = {
                "ID" : filename
            }
            
            file_data.append(info)

            storage.seek(0)
            json.dump(file_data, storage, indent=4)
            storage.close()

        
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