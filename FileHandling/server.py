import os
from socket import *
import json
from threading import *

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    while True:
        try:
            option = client.recv(1024).decode(FORMAT)
        except:
            break
        if not option:
            break
        print(option)

        if option == "1":
            file = open("receivedFile.txt", "wb")
            data = client.recv(2048)
            while data:
                file.write(data)
                data = client.recv(2048)
            file.close()
        elif option == "2":
            file = open("downloadFile.txt", "rb")
            data = file.read(2048)
            while data:
                client.sendall(data)
                data = file.read(2048)
            file.close()

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

SERVER.listen(5)
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=accept_incoming_connections)

ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()