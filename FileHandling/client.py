from socket import *

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

while True:
    option = input("Enter your option: ")
    client.sendall(option.encode(FORMAT))

    if option == "1":
        file = open("sendFile.txt", "rb")
        data = file.read(2048)
        while data:
            client.sendall(data)
            data = file.read(2048)
        file.close()
    elif option == "2":
        file = open("downloadedFile.txt", "wb")
        data = client.recv(2048)
        while data:
            file.write(data)
            data = client.recv(2048)
        file.close()
