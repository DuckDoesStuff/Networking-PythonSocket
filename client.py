from socket import *
from threading import *
from ipaddress import *
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class SignIn:
    def __init__(self, frame, socket):
        self.socket = socket
        self.frame = Frame(frame, width=350, height=350, bg='white')
        self.frame.place(x=0, y=0)

        # Header title
        self.heading = Label(self.frame, text='Sign in', fg='#06283D',
                                bg='white', font=('Roboto', 19, 'bold'))
        self.heading.place(x=130, y=5)


        # Username input box
        self.username = Label(self.frame,text="Username", bg='white', font=('Roboto', 13))
        self.username.place(x=25, y=60)
        
        self.user = Entry(self.frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Roboto', 13))
        self.user.place(x=25, y=90)


        # Password input box
        self.password = Label(self.frame,text="Password", bg='white', font=('Roboto', 13))
        self.password.place(x=25, y=130)

        self.pswd = Entry(self.frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Roboto', 13))
        self.pswd.place(x=25, y=150)


        # Signin button
        self.btn = Button(self.frame, width=10, text="Sign in", activebackground='red', 
                        font=('Roboto', 11), bd=0, command=self.sign_in, bg='black', fg='white')
        self.btn.place(x=138, y=270)


        # Need an account?
        Label(self.frame, text="Don't have an account?", 
            bg='white', font=('Roboto', 11)).place(x=105, y=295)

        self.sgup = Button(self.frame, width=10, text="Sign up", activebackground='red', 
                        font=('Roboto', 11), bd=0, bg='black', fg='white', command=self.sign_up)
        self.sgup.place(x=138, y=320)
    
    def sign_in(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()

        if self.name == '' or self.psw == '':
            print("Fields can't be empty")
            return
        
        # Notify server client is logging in
        option = "SIGNIN"
        self.socket.sendall(option.encode(FORMAT))
        self.socket.recv(1024)

        # Sending client's data
        self.socket.sendall(self.name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(self.psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign in data sent")

        response = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(response.encode(FORMAT))

        if response != "SIGNEDIN":
            announce = Label(self.frame, text=response, bg='white', font=('Roboto', 13))
            announce.place(x=55, y=175)
        else:
            self.frame.destroy()
            MainHome(root, self.socket)

    def sign_up(self):
        self.frame.destroy()
        SignUp(root, self.socket)

class SignUp:
    def __init__(self, frame, socket):
        self.socket = socket
        self.frame = Frame(frame, width=350, height=350, bg='white')
        self.frame.place(x=0, y=0)

        # Header title
        self.heading = Label(self.frame, text='Sign up', fg='#06283D',
                                bg='white', font=('Roboto', 19, 'bold'))
        self.heading.place(x=130, y=5)


        # Username input box
        self.username = Label(self.frame,text="Username", bg='white', font=('Roboto', 13))
        self.username.place(x=25, y=60)
        
        self.user = Entry(self.frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Roboto', 13))
        self.user.place(x=25, y=90)


        # Password input box
        self.password = Label(self.frame,text="Password", bg='white', font=('Roboto', 13))
        self.password.place(x=25, y=130)

        self.pswd = Entry(self.frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Roboto', 13))
        self.pswd.place(x=25, y=150)


        # Signup button
        self.btn = Button(self.frame, width=10, text="Sign up", activebackground='red', 
                        font=('Roboto', 11), bd=0, command=self.sign_up, bg='black', fg='white')
        self.btn.place(x=138, y=270)


        # Already have an accout?
        Label(self.frame, text="Already have an account?", 
            bg='white', font=('Roboto', 11)).place(x=100, y=295)

        self.sgin = Button(self.frame, width=10, text="Sign in", activebackground='red', 
                        font=('Roboto', 11), bd=0, bg='black', fg='white', command=self.sign_in)
        self.sgin.place(x=138, y=320)
    
    def sign_up(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()

        if self.name == 'Username':
            print("Invalid username")
            return
        if self.psw == '' or self.name == '':
            print("Fields can't be empty")
            return

        # Notify server client is signing up
        option = "SIGNUP"
        self.socket.sendall(option.encode(FORMAT))
        self.socket.recv(1024)

        # Sending client's data
        self.socket.sendall(self.name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(self.psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign up data sent")

        response = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(response.encode(FORMAT))

        if response != "SIGNEDUP":
            announce = Label(self.frame, text=response, bg='white', font=('Roboto', 13))
            announce.place(x=80, y=175)
        else:
            print("Signed up success")

    def sign_in(self):
        self.frame.destroy()
        SignIn(root, self.socket)

class MainHome:
    def __init__(self, frame, socket):
        self.socket = socket
        self.frame = Frame(frame, width=925, height=500)
        self.frame.pack()
        self.frame.place(x=0, y=0)

        self.browse_file = Button(self.frame, width=10, text="Browse files", activebackground='red', 
                        font=('Roboto', 11), bd=0, bg='black', fg='white', command=self.browse_file)
        self.browse_file.place(x=0, y=100)

        # img = ImageTk.PhotoImage(file="img.png")
        # self.img = Label(self.frame, image = img, bg='white')
        # self.img.place(x=30, y=100)

    def browse_file(self):
        self.filepath = filedialog.askopenfilename(initialdir = "/", 
                title = "Select a File")

        file_open = Label(self.frame, text = self.filepath, fg='#06283D',
                                bg='white', font=('Roboto', 19, 'bold'))
        file_open.place(x=0, y=0)

        upload = Button(self.frame, width=10, text="Upload", activebackground='red', 
                        font=('Roboto', 11), bd=0, bg='black', fg='white', command=self.upload_file)
        upload.place(x=0, y=150)
    def upload_file(self):
        if self.filepath:# will not execute if no file is opened
            self.socket.sendall("UPLOAD".encode(FORMAT))
            self.socket.recv(1024)
            
            self.socket.sendall(self.filepath.encode(FORMAT))
            self.socket.recv(1024)
            print("Uploading file")

            file = open(self.filepath, "rb")
            data = file.read(2048)
            while data:
                self.socket.sendall(data)
                self.socket.recv(2048)
                data = file.read(2048)
            self.socket.sendall("DONE".encode(FORMAT))
            print("Upload completed")
            file.close()



HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

root = Tk()
root.geometry('925x500+300+200')        #Set window size and position
root.resizable(False, False)            #Disable X and Y resizing
root.title('Demo')

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

signin = SignIn(root, client_socket)


root.mainloop()