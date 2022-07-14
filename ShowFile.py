import cv2
import os
from socket import *
from threading import *
from tkinter import *
import shutil
from pathlib import Path

BUFFER_SIZE = 300000
FORMAT = 'utf8'

class ShowFile:
    def __init__(self, socket, file_id):
        self.root = Tk()
        self.root.geometry("120x120")
        self.root.title("Viewing file")

        self.socket = socket
        self.frame = Frame(self.root, width=120, height=120, bg='white')
        self.frame.pack()
        self.frame.place(x=0, y=0)

        # Asking server to send file data
        self.socket.sendall("VIEW_FILE".encode(FORMAT))
        self.socket.recv(1024)

        # Sending File's ID
        self.socket.sendall(str(file_id).encode(FORMAT))
        self.socket.recv(1024)

        # Receiving File's data
        self.file_name = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(self.file_name.encode(FORMAT))

        self.save_temp()

        # View image
        if not os.path.splitext(self.file_name)[1] == ".txt":
            path = './temp/' + self.file_name
            img = cv2.imread(path)
            cv2.imshow('Viewing Image', img)

        # Download button
        dwn_btn = Button(self.frame, width=10, text="Download", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#009156', fg='white', command=self.download_file)
        dwn_btn.place(x=13, y=20)


        # Close window button
        close_btn = Button(self.frame, width=10, text="Close", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#009156', fg='white', command=self.close_window)
        close_btn.place(x=13, y=50)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.root.mainloop()
        
    
    def save_temp(self):
        self.socket.sendall("DOWNLOAD".encode(FORMAT))
        self.socket.recv(1024)

        # Send file name to server
        self.socket.sendall(self.file_name.encode(FORMAT))
        self.socket.recv(1024)

        cwd = os.getcwd()
        down_path = "./temp/"
        if not os.path.exists(down_path):
            os.mkdir(down_path)
        os.chdir(down_path)

        # Receiving file data
        filesize = int(self.socket.recv(1024).decode(FORMAT))
        self.socket.sendall(str(filesize).encode(FORMAT))
        
        file = open(self.file_name, "wb")
        recved = 0
        while True:
            data = self.socket.recv(BUFFER_SIZE)
            recved += len(data)
            if recved >= filesize:
                file.write(data)
                break
            file.write(data)
        file.close()

        os.chdir(cwd)
    
    def download_file(self):
        self.socket.sendall("DOWNLOAD".encode(FORMAT))
        self.socket.recv(1024)

        # Send file name to server
        self.socket.sendall(self.file_name.encode(FORMAT))
        self.socket.recv(1024)

        cwd = os.getcwd()
        down_path = str(Path.home() / "Downloads")
        if not os.path.exists(down_path):
            os.mkdir(down_path)
        os.chdir(down_path)

        # Receiving file data
        filesize = int(self.socket.recv(1024).decode(FORMAT))
        self.socket.sendall(str(filesize).encode(FORMAT))
        
        file = open(self.file_name, "wb")
        recved = 0
        while True:
            data = self.socket.recv(BUFFER_SIZE)
            recved += len(data)
            if recved >= filesize:
                file.write(data)
                break
            file.write(data)
        file.close()

        os.chdir(cwd)
        self.close_window()

    def clear_folder(self):
        shutil.rmtree("./temp/")
        os.makedirs("./temp/", exist_ok=True)

    def close_window(self):
        self.clear_folder()
        self.root.destroy()
