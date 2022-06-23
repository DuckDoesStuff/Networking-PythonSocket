from socket import *
from threading import *
from ipaddress import *
from tkinter import *

class SignIn:
    def __init__(self, frame, socket):
        self.frame = Frame(frame, width=350, height=350, bg='white')
        self.frame.place(x=0, y=0)
        self.socket = socket
        # Header title
        self.heading = Label(self.frame, text='Sign in', fg='#06283D',
                                bg='#DFF6FF', font=('Roboto', 19, 'bold'))
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
        self.sgup = Button(self.frame, width=10, text="Sign up", activebackground='red', 
                        font=('Roboto', 11), bd=0, bg='black', fg='white', command=self.sign_up)
        self.sgup.place(x=138, y=320)
    
    def sign_in(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()

        if self.name == 'Username' or self.psw == 'Password':
            print("Fields can't be empty")
            return
        
        # Notify server client is logging in
        option = "LOGIN"
        self.socket.sendall(option.encode(FORMAT))

        # Sending client's data
        self.socket.sendall(self.name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(self.psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign in data sent")

        response = self.socket.recv(1024).decode(FORMAT)

        if response != "LOGGEDIN":
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
                                bg='#DFF6FF', font=('Roboto', 19, 'bold'))
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
        self.sgin = Button(self.frame, width=10, text="Sign in", activebackground='red', 
                        font=('Roboto', 11), bd=0, bg='black', fg='white', command=self.sign_in)
        self.sgin.place(x=138, y=320)
    
    def sign_up(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()

        if self.name == 'Username' or self.psw == 'Password':
            print("Fields can't be empty")
            return

        # Notify server client is signing up
        option = "SIGNUP"
        self.socket.sendall(option.encode(FORMAT))

        # Sending client's data
        self.socket.sendall(self.name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(self.psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign up data sent")

        response = self.socket.recv(1024)

        if response != "SIGNEDUP":
            announce = Label(self.frame, text=response, bg='white', font=('Roboto', 13))
            announce.place(x=80, y=175)
        else:
            pass

    def sign_in(self):
        self.frame.destroy()
        SignIn(root, self.socket)

class MainHome:
    def __init__(self, frame, socket):
        self.socket = socket
        self.frame = Frame(frame, width=925, height=500, bg='red')
        self.frame.place(x=0, y=0)

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

root = Tk()
root.geometry('925x500+300+200')        #Set window size and position
root.resizable(False, False)            #Disable X and Y resizing
root.title('Testing')

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

signin = SignIn(root, client_socket)


root.mainloop()