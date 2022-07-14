import cv2
import json
import os
from socket import *
from threading import *
from tkinter import *
from tkinter import filedialog
import tkinter
import shutil

class SignIn:
    def __init__(self, frame, socket):
        self.socket = socket

        bg = PhotoImage(file = './images/signin.png')
        title_label = Label(root,image=bg)
        title_label.image = bg
        title_label.pack(fill='both', expand='yes')
        title_label.place(x=-2,y=-2)
        
        self.frame = Frame(frame, width=350, height=350)
        self.frame.place(x=100, y=50)

        bg = PhotoImage(file = './images/signin.png')
        title_label = Label(self.frame,image=bg)
        title_label.image = bg
        title_label.pack(fill='both', expand='yes')
        title_label.place(x=-102,y=-52)
        
        self.user = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.user.place(x=121, y=139)

        self.pswd = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.pswd.place(x=121, y=194)

        # Sign in button
        btn = Button(self.frame, width=10, text="Sign in", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, command=self.sign_in, bg='#009156', fg='white')
        btn.place(x=145, y=260)

        # Sign up button
        sign_up_btn = Button(self.frame, width=10, text="Sign up", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#009156', fg='white', command=self.sign_up)
        sign_up_btn.place(x=145, y=310)
    
    def sign_in(self):
        name = self.user.get()
        psw = self.pswd.get()

        if name == '' or psw == '':
            print("Fields can't be empty")
            return
        
        # Notify server client is logging in
        option = "SIGN_IN"
        self.socket.sendall(option.encode(FORMAT))
        self.socket.recv(1024)

        # Sending client's data
        self.socket.sendall(name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign in data sent")

        response = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(response.encode(FORMAT))

        if response != "SUCCESS":
            tkinter.messagebox.showinfo("Announcement", "Incorrect username or password!")
        else:
            self.frame.destroy()
            MainHome(root, self.socket)

    def sign_up(self):
        self.frame.destroy()
        SignUp(root, self.socket)

class SignUp:
    def __init__(self, frame, socket):
        self.socket = socket

        bg = PhotoImage(file = './images/signup.png')
        title_label = Label(root,image=bg)
        title_label.image = bg
        title_label.pack(fill='both', expand='yes')
        title_label.place(x=-2,y=-2)
        
        self.frame = Frame(frame, width=350, height=350)
        self.frame.place(x=100, y=50)

        bg = PhotoImage(file = './images/signup.png')
        title_label = Label(self.frame,image=bg)
        title_label.image = bg
        title_label.pack(fill='both', expand='yes')
        title_label.place(x=-102,y=-52)
        
        self.user = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.user.place(x=121, y=139)

        self.pswd = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.pswd.place(x=121, y=194)


        # Sign up button
        btn = Button(self.frame, width=10, text="Sign up", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, command=self.sign_up, bg='#009156', fg='white')
        btn.place(x=145, y=260)

        # Sign in button
        sign_in_btn = Button(self.frame, width=10, text="Sign in", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#009156', fg='white', command=self.sign_in)
        sign_in_btn.place(x=145, y=310)
    
    def sign_up(self):
        name = self.user.get()
        psw = self.pswd.get()

        if name == 'Username':
            print("Invalid username")
            return
        if psw == '' or name == '':
            print("Fields can't be empty")
            return

        # Notify server client is signing up
        option = "SIGN_UP"
        self.socket.sendall(option.encode(FORMAT))
        self.socket.recv(1024)

        # Sending client's data
        self.socket.sendall(name.encode(FORMAT))
        self.socket.recv(1024)#? couldn't receive anything

        self.socket.sendall(psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign up data sent")

        response = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(response.encode(FORMAT))

        if response == "1":
            tkinter.messagebox.showinfo("Announcement", "Sign up successful please return to login page")
        elif response == "-1":
            tkinter.messagebox.showinfo("Announcement", "Invalid username")
        elif response == "-2":
            tkinter.messagebox.showinfo("Announcement", "Invalid password")
        elif response == "-3":
            tkinter.messagebox.showinfo("Announcement", "Username already exist")

    def sign_in(self):
        self.frame.destroy()
        SignIn(root, self.socket)

class TakeNote:
    def __init__(self, socket):
        self.root = Toplevel()
        self.root.geometry("925x500")
        self.root.title("New note")

        self.socket = socket
        self.frame = Frame(self.root, width=950, height=500)
        self.frame.place(x=0, y=0)

        bg = PhotoImage(file = './images/note_up.png')
        background = Label(self.frame,image=bg)
        background.image = bg
        background.pack(fill='both', expand='yes')
        background.place(x=0,y=0)

        # Topic entry box
        self.topicEnt = Entry(self.frame, width=55, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.topicEnt.place(x=210, y=95)

        # Content text box
        self.contentEnt = Text(self.frame, width=55, height=5, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.contentEnt.place(x=210, y=170)

        newNote = Button(self.frame, width=10, text="New note", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, command=self.upload_note, bg='#009156', fg='white')
        newNote.place(x=210, y=390)

        # Cancel button
        cancel = Button(self.frame, width=10, text="Cancel", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, command=self.cancel, bg='white', fg='#009156')
        cancel.place(x=800, y=450)

        # Closing window will cancel sending note
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

        self.root.mainloop()

    def upload_note(self):
        topic = self.topicEnt.get()
        content = self.contentEnt.get(1.0, END)

        if topic == "" or content == "\n":
            tkinter.messagebox.showinfo("Announcement", "Topic or content can't be empty")
            self.cancel()
            return

        self.socket.sendall("ADD_NOTE".encode(FORMAT))
        self.socket.recv(1024)
        
        self.socket.sendall(topic.encode(FORMAT))
        self.socket.recv(BUFFER_SIZE)

        self.socket.sendall(content.encode(FORMAT))
        self.socket.recv(BUFFER_SIZE)

        self.root.destroy()
        return
    def cancel(self):
        self.socket.sendall("CANCEL".encode(FORMAT))
        self.socket.recv(1024)

        print("Cancel note")
        self.root.destroy()
        return

class ShowNote:
    def __init__(self, socket, note_id):
        self.root = Toplevel()
        self.root.geometry("925x500")
        self.root.title("Viewing note")

        self.socket = socket
        self.frame = Frame(self.root, width=925, height=500)
        self.frame.pack()
        self.frame.place(x=0, y=0)

        bg = PhotoImage(file = './images/note_load.png')
        background = Label(self.frame,image=bg)
        background.image = bg
        background.pack(fill='both', expand='yes')
        background.place(x=0,y=0)

        # Asking server to send note data
        self.socket.sendall("VIEW_NOTE".encode(FORMAT))
        self.socket.recv(1024)

        # Sending Note's ID
        self.socket.sendall(str(note_id).encode(FORMAT))
        self.socket.recv(1024)

        # Receiving Note's info
        topic = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(topic.encode(FORMAT))

        content = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(content.encode(FORMAT))

        # Showing Note's topic and content
        view_topic = Label(self.frame, width=20, text=topic, 
                            font=('Roboto', 14),bg='white', fg='black',anchor=W)
        view_topic.place(x=76, y=95)

        view_content = Label(self.frame, width=40, text=content, 
                            font=('Roboto', 12), bg='white', fg='black',anchor=W)
        view_content.place(x=76, y=168)

        # Close Note window
        close_btn = Button(self.frame, width=10, text="Close", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='white', fg='#009156', command=self.close_window)
        close_btn.place(x=53, y=446)

        self.root.mainloop()

    def close_window(self):
        self.root.destroy()

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
        down_path = "C:/Users/Admin/Desktop/Downloads"
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
        self.clear_folder()

    def clear_folder(self):
        shutil.rmtree("./temp/")
        os.makedirs("./temp/", exist_ok=True)

    def close_window(self):
        self.clear_folder()
        self.root.destroy()

class MainHome:
    def __init__(self, frame, socket):
        self.socket = socket
        self.frame = Frame(frame, width=925, height=500)
        self.frame.pack()
        self.frame.place(x=0, y=0)
        self.filepath = ""

        bg = PhotoImage(file = './images/main_menu.png')
        title_label = Label(self.frame,image=bg)
        title_label.image = bg
        title_label.pack(fill='both', expand='yes')
        title_label.place(x=0,y=0)

        # New text file button
        browse_text = Button(self.frame, width=10, text="Browse text", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#168E60', fg='white', command=self.add_text)
        browse_text.place(x=346, y=444)

        # New image file button
        browse_image = Button(self.frame, width=10, text="Browse image", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#168E60', fg='white', command=self.add_image)
        browse_image.place(x=217, y=444)

        # Upload note button
        upload_note_btn = Button(self.frame, width=10, text="Upload note", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#04C582', fg='white', command=self.upload_note)
        upload_note_btn.place(x=36, y=444)

        # Upload file button
        upload_file_btn = Button(self.frame, width=10, text="Upload file", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#04C582', fg='white', command=self.upload_file)
        upload_file_btn.place(x=475, y=444)

        # Refresh listbox
        refresh = Button(self.frame, width=10, text="Refresh", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='white', fg='#04C582', command=self.update_list)
        refresh.place(x=782, y=444)

        # Note list handling
        self.notelist = Listbox(self.frame, width=30, height=10, bd=0, font=('Roboto', 16),
                                highlightthickness=0, selectbackground='#D4D4D4')
        self.notelist.place(x=42, y=70)

        self.notelist.bind("<<ListboxSelect>>", self.show_note)
        

        # File list handling
        self.filelist = Listbox(self.frame, width=30, height=10, bd=0, font=('Roboto', 16),
                                highlightthickness=0, selectbackground='#D4D4D4')
        self.filelist.place(x=485, y=70)

        self.filelist.bind("<<ListboxSelect>>", self.show_file)
        

        self.update_list()

    def show_note(self, event):
        selection = event.widget.curselection()
        note_id = selection[0] + 1
        
        ShowNote(self.socket, note_id)
    
    def show_file(self, event):
        selection = event.widget.curselection()
        file_id = selection[0] + 1

        ShowFile(self.socket, file_id)
        
    def update_list(self):
        print("Updating list")
        # Asking for notes list
        self.socket.sendall("NOTE_LIST".encode(FORMAT))
        self.socket.recv(1024)

        self.user_notes = json.loads(self.socket.recv(1024).decode(FORMAT))
        self.notelist.delete(0, END)

        index = 1
        for i in self.user_notes:
            self.notelist.insert(index, i['topic'])
            index += 1  
        
        # Asking for files list
        self.socket.sendall("FILE_LIST".encode(FORMAT))
        self.socket.recv(1024)

        self.user_files = json.loads(self.socket.recv(1024).decode(FORMAT))
        self.filelist.delete(0, END)

        index = 1
        for i in self.user_files:
            self.filelist.insert(index, i['name'])
            index += 1

    def add_text(self):
        self.upld_img = False
        self.filepath = filedialog.askopenfilename(initialdir = "/", 
                title = "Select a File", filetypes=[("Text files", ".txt")])
    
    def add_image(self):
        self.upld_img = True
        self.filepath = filedialog.askopenfilename(initialdir = "/", 
                title = "Select a File", filetypes=[("Image files", ".png .jpg")])

    def upload_file(self):
        if self.filepath:# will not execute if no file is opened
            self.socket.sendall("ADD_FILE".encode(FORMAT))
            self.socket.recv(1024)

            if self.upld_img:
                self.socket.sendall("IMAGE".encode(FORMAT))
            else:
                self.socket.sendall("TEXT".encode(FORMAT))
            self.socket.recv(1024)
            
            filesize = os.path.getsize(self.filepath)
            info = f"{self.filepath}{SEPARATOR}{filesize}"
            self.socket.sendall(info.encode(FORMAT))

            print("Uploading file")

            file = open(self.filepath, "rb")
            while True:
                data = file.read(BUFFER_SIZE)
                if not data:
                    break
                self.socket.sendall(data)
                
            print("Upload completed")
            file.close()
            self.filepath = ""

    def upload_note(self):
        self.socket.sendall("ADD_NOTE".encode(FORMAT))
        self.socket.recv(1024)

        TakeNote(self.socket)

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 300000
HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

root = Tk()
root.geometry('925x500+300+200')        #Set window size and position
root.resizable(False, False)            #Disable X and Y resizing
root.title('E-Note')

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

signin = SignIn(root, client_socket)


root.mainloop()