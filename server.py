from math import ceil
from socket import *
from threading import *
import json
import os

def check(username, password):
    if len(username) < 5:
        return -1
    if len(password) < 3:
        return -2
    return 1

def new_file(client, client_name):
    info = client.recv(1024).decode(FORMAT).split(SEPARATOR)
    filepath = info[0]
    filesize = int(info[1])

    filename = os.path.basename(filepath)
    print(filename)
    print(filepath)

    cwd = os.getcwd()

    upld_path = "./storage/" + client_name
    if not os.path.exists(upld_path):
        os.mkdir(upld_path)
    os.chdir(upld_path)

    file = open(filename, "wb")
    recved = 0
    while True:
        data = client.recv(BUFFER_SIZE)
        recved += len(data)
        if recved >= filesize:
            break
        file.write(data)
    file.close()
    os.chdir(cwd)
    
    print(filename)
    print("Receiving completed")

def new_note(client, client_name):
    note_file = open("./storage/" + client_name + "/note.json", "r+")
    note_data = json.load(note_file)

    msg = client.recv(1024).decode(FORMAT)
    client.sendall(msg.encode(FORMAT))
    if msg == "CANCEL":
        note_file.close()
        return
    
    topic = client.recv(BUFFER_SIZE).decode(FORMAT)
    client.sendall(topic.encode(FORMAT))

    content = client.recv(BUFFER_SIZE).decode(FORMAT)
    client.sendall(content.encode(FORMAT))

    take_note = {
        "id" : len(note_data) + 1,
        "topic" : topic,
        "content" : content
    }

    note_data.append(take_note)

    note_file.seek(0)
    json.dump(note_data, note_file, indent=4)    

    note_file.close()

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
            print("Signing in")
            client.sendall(option.encode(FORMAT))

            client_name = client.recv(1024).decode(FORMAT)
            client.sendall(client_name.encode(FORMAT))

            client_psw = client.recv(1024).decode(FORMAT)
            client.sendall(client_psw.encode(FORMAT))

            print(client_name)
            print(client_psw)

            f = open('accounts.json', 'r')
            acc_data = json.load(f)
            f.close()
            
            signedIn = False
            for user in acc_data:
                if user['username'] == client_name:
                    if user['password'] == client_psw:
                        print("Sign success")
                        client.sendall("SIGNEDIN".encode(FORMAT))
                        signedIn = True
                    else:
                        print("Signin failed")
                    break
            
            if not signedIn:
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
            acc_data = json.load(f)
            
            checkValid = check(client_name, client_psw)
            if checkValid == 1:
                for user in acc_data:
                    if user['username'] == client_name:
                        print('Username already exist')
                        f.close()
                        checkValid = -3
                        break
            
            if checkValid == 1:
                # Append new user's account to database
                info = {
                    "username" : client_name,
                    "password" : client_psw
                }

                acc_data.append(info)

                f.seek(0)
                json.dump(acc_data, f, indent=4)
                f.close()

                # Init user's folders
                newfolder = "./storage/" + client_name
                os.mkdir(newfolder)
                init_list = []
                file = open("./storage/" + client_name + "/note.json", "w")
                file.write(json.dumps(init_list, indent=4))
                file.close()

                init_list = []
                file = open("./storage/" + client_name + "/directory.json", "w")
                file.write(json.dumps(init_list, indent=4))
                file.close()

                print("Create account succesfully")

                client.sendall(str(checkValid).encode(FORMAT))
            else:
                client.sendall(str(checkValid).encode(FORMAT))
            client.recv(1024)

        elif option == "UPLOAD":
            client.sendall(option.encode(FORMAT))
            new_file(client, client_name)
        
        elif option == "ADD_NOTE":
            client.sendall(option.encode(FORMAT))
            new_note(client, client_name)

                
    print(str(addresses[client][0]) + ":" + str(addresses[client][1]) + " has disconnected")
    client.close()
       
clients = {}
addresses = {}

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 10240
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