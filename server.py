from socket import *
from threading import *
import json
import os

special_char = ["~","`","!","@","#","$","%","^","&","*","(",")",
                "-","_","+","=","{","}","[","]",":",";","\"",
                "'","<",">","/","?","|","\\",".",","]
def checkSpecialChar(username):
    if any(x in username for x in special_char):
        return True
    else: 
        return False

def check(username, password):
    if len(username) < 5 or checkSpecialChar(username):
        return -1
    if len(password) < 3:
        return -2
    return 1

def saveToJson(filename, filetype):
    file = open("directory.json", "r+")
    file_data = json.load(file)
    info = {
        "id" : len(file_data) + 1,
        "type" : filetype,
        "name" : filename
    }
    file_data.append(info)
    file.seek(0)
    json.dump(file_data, file, indent=4)
    file.close()

def add_file(client, client_name):
    upld_type = client.recv(1024).decode(FORMAT)
    client.sendall(upld_type.encode(FORMAT))

    info = client.recv(1024).decode(FORMAT).split(SEPARATOR)
    filepath = info[0]
    filesize = int(info[1])

    filename = os.path.basename(filepath)
    print(filesize)
    print(filename)

    cwd = os.getcwd()

    upld_path = "./storage/" + client_name
    if not os.path.exists(upld_path):
        os.mkdir(upld_path)
    os.chdir(upld_path)

    if upld_type == "IMAGE":
        saveToJson(filename, "image")
    elif upld_type == "TEXT":
        saveToJson(filename, "text")

    file = open(filename, "wb")
    recved = 0
    while True:
        data = client.recv(BUFFER_SIZE)
        recved += len(data)
        if recved >= filesize:
            file.write(data)
            break
        file.write(data)
    file.close()
    os.chdir(cwd)
    
    print("Receiving completed")

def add_note(client, client_name):
    note_file = open("./storage/" + client_name + "/note.json", "r+")
    note_data = json.load(note_file)

    msg = client.recv(1024).decode(FORMAT)
    client.sendall(msg.encode(FORMAT))
    if msg == "CANCEL":
        note_file.close()
        print(msg)
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

def note_list(client, client_name):
    note_path = "./storage/" + client_name + "/note.json"
    file = open(note_path, "r")
    user_notes = json.load(file)
    client.sendall((json.dumps(user_notes)).encode(FORMAT))

    file.close()

def file_list(client, client_name):
    note_path = "./storage/" + client_name + "/directory.json"
    file = open(note_path, "r")
    user_notes = json.load(file)
    client.sendall((json.dumps(user_notes)).encode(FORMAT))

    file.close()

def view_note(client, client_name):
    note_id = int(client.recv(1024).decode(FORMAT))
    client.sendall(str(note_id).encode(FORMAT))

    note_path = "./storage/" + client_name + "/note.json"
    file = open(note_path, "r")
    note_data = json.load(file)
    file.close()

    for note in note_data:
        if note['id'] == note_id:
            client.sendall(note['topic'].encode(FORMAT))
            client.recv(1024)

            client.sendall(note['content'].encode(FORMAT))
            client.recv(1024)
            break

def view_file(client, client_name):
    file_id = int(client.recv(1024).decode(FORMAT))
    client.sendall(str(file_id).encode(FORMAT))

    file_path = "./storage/" + client_name + "/directory.json"
    file = open(file_path, "r")
    file_data = json.load(file)
    file.close()

    for file in file_data:
        if file['id'] == file_id:
            client.sendall(file['name'].encode(FORMAT))
            client.recv(1024)
            # Something something
            break  

def download_file(client, client_name):
    filename = client.recv(1024).decode(FORMAT)
    client.sendall(filename.encode(FORMAT))

    cwd = os.getcwd()
    os.chdir("./storage/" + client_name)

    file = open(filename, "rb")

    filesize = os.path.getsize(filename)
    client.sendall(str(filesize).encode(FORMAT))
    client.recv(1024)

    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        client.sendall(data)    

    file.close()
    os.chdir(cwd)
    print("Download completed")

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
        if option == "SIGN_IN":
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
                        client.sendall("SUCCESS".encode(FORMAT))
                        signedIn = True
                    else:
                        print("Signin failed")
                    break
            
            if not signedIn:
                client.sendall("Incorrect username or password".encode(FORMAT))
            client.recv(1024)

        elif option == "SIGN_UP":
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

        elif option == "ADD_FILE":
            client.sendall(option.encode(FORMAT))
            add_file(client, client_name)
        
        elif option == "ADD_NOTE":
            client.sendall(option.encode(FORMAT))
            add_note(client, client_name)
        
        elif option == "NOTE_LIST":
            client.sendall(option.encode(FORMAT))
            note_list(client, client_name)
        
        elif option == "VIEW_NOTE":
            client.sendall(option.encode(FORMAT))
            view_note(client, client_name)

        elif option == "FILE_LIST":
            client.sendall(option.encode(FORMAT))
            file_list(client, client_name)
        
        elif option == "VIEW_FILE":
            client.sendall(option.encode(FORMAT))
            view_file(client, client_name)
        
        elif option == "DOWNLOAD":
            client.sendall(option.encode(FORMAT))
            download_file(client, client_name)
                
    print(str(addresses[client][0]) + ":" + str(addresses[client][1]) + " has disconnected")
    client.close()
       
clients = {}
addresses = {}

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 300000
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