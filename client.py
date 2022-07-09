from socket import *
from threading import *
from ipaddress import *
from tkinter import *
from PIL import Image, ImageTk

class SignIn:
    def __init__(self, frame, socket):
        self.socket = socket

        self.bg = PhotoImage(file = './images/signin.png')
        self.my_label = Label(root,image=self.bg)
        self.my_label.image = self.bg
        self.my_label.pack(fill='both', expand='yes')
        self.my_label.place(x=-2,y=-2)
        
        self.frame = Frame(frame, width=350, height=350)
        self.frame.place(x=100, y=50)

        self.bg = PhotoImage(file = './images/signin.png')
        self.my_label = Label(self.frame,image=self.bg)
        self.my_label.image = self.bg
        self.my_label.pack(fill='both', expand='yes')
        self.my_label.place(x=-102,y=-52)
        
        self.user = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.user.place(x=121, y=139)

        self.pswd = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.pswd.place(x=121, y=194)


        # Signin button
        self.btn = Button(self.frame, width=10, text="Sign in", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, command=self.sign_in, bg='#009156', fg='white')
        self.btn.place(x=145, y=260)

        self.sgup = Button(self.frame, width=10, text="Sign up", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#009156', fg='white', command=self.sign_up)
        self.sgup.place(x=145, y=310)
    
    def sign_in(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()

        if self.name == '' or self.psw == '':
            print("Fields can't be empty")
            return
        
        # Notify server client is logging in
        option = "SIGNIN"
        self.socket.sendall(option.encode(FORMAT))

        # Sending client's data
        self.socket.sendall(self.name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(self.psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign in data sent")

        response = self.socket.recv(1024).decode(FORMAT)

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

        self.bg = PhotoImage(file = './images/signup.png')
        self.my_label = Label(root,image=self.bg)
        self.my_label.image = self.bg
        self.my_label.pack(fill='both', expand='yes')
        self.my_label.place(x=-2,y=-2)
        
        self.frame = Frame(frame, width=350, height=350)
        self.frame.place(x=100, y=50)

        self.bg = PhotoImage(file = './images/signup.png')
        self.my_label = Label(self.frame,image=self.bg)
        self.my_label.image = self.bg
        self.my_label.pack(fill='both', expand='yes')
        self.my_label.place(x=-102,y=-52)
        
        self.user = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.user.place(x=121, y=139)

        self.pswd = Entry(self.frame, width=19, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.pswd.place(x=121, y=194)


        # Signup button
        self.btn = Button(self.frame, width=10, text="Sign up", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, command=self.sign_up, bg='#009156', fg='white')
        self.btn.place(x=145, y=260)

        self.sgin = Button(self.frame, width=10, text="Sign in", activebackground='#ffcd6e', 
                        font=('Roboto', 11), bd=0, bg='#009156', fg='white', command=self.sign_in)
        self.sgin.place(x=145, y=310)
    
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

        # Sending client's data
        self.socket.sendall(self.name.encode(FORMAT))
        self.socket.recv(1024)#? couldn't receive anything

        self.socket.sendall(self.psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Sign up data sent")

        response = self.socket.recv(1024).decode(FORMAT)

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
        self.frame = Frame(frame, width=925, height=500, bg='red')
        self.frame.place(x=0, y=0)

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