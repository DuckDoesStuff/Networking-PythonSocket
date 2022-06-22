from socket import *
from threading import *
from ipaddress import *
from tkinter import *

root = Tk()
root.geometry('925x500+300+200')        #Set window size and position
root.resizable(False, False)            #Disable X and Y resizing
root.title('Testing')

class SignIn:
    def __init__(self, frame, socket):
        frame = Frame(frame, width=350, height=350, bg='white')
        frame.place(x=0, y=0)
        self.socket = socket
        # Header title
        self.heading = Label(frame, text='Sign in', fg='#06283D',
                                bg='#DFF6FF', font=('Consolas', 19, 'bold'))
        self.heading.place(x=130, y=5)

        # Username input box
        self.user = Entry(frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Consolas', 13))
        self.user.place(x=25, y=90)
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', self.on_enter_user)
        self.user.bind('<FocusOut>', self.on_leave_user)

        # Password input box
        self.pswd = Entry(frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Consolas', 13))
        self.pswd.place(x=25, y=150)
        self.pswd.insert(0, 'Password')
        self.pswd.bind('<FocusIn>', self.on_enter_pswd)
        self.pswd.bind('<FocusOut>', self.on_leave_pswd)

        # Signin button
        self.btn = Button(frame, width=10, text="Sign in", activebackground='red', 
                        font=('Consolas', 11), bd=0, command=self.sign_in, bg='black', fg='white')
        self.btn.place(x=138, y=270)

        # Need an account?
        self.sign_up = SignUp(root, self.socket)
        # self.label = Label(frame, text="Need an account?", font=("Consolas", 9), fg='black', bg='#1363DF', bd=0)
        # self.label.place(x=122, y=295)
       

    def on_enter_user(self, e):
        self.name = self.user.get()
        if self.name == 'Username':
            self.user.delete(0, 'end')

    def on_leave_user(self, e):
        self.name = self.user.get()
        if self.name == '':
            self.user.insert(0, 'Username')
        # self.user.unbind('<FocusOut>')

    def on_enter_pswd(self, e):
        self.psw = self.pswd.get()
        if self.psw == 'Password':
            self.pswd.delete(0, 'end')

    def on_leave_pswd(self, e):
        self.psw = self.pswd.get()
        if self.psw == '':
            self.pswd.insert(0, 'Password')        
        # self.pswd.unbind('<FocusOut>')
    
    def sign_in(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()

        if self.name == 'Username' or self.psw == 'Password':
            print("Fields can't be empty")
            return
        
        # Notify server client is logging in
        option = "LOGIN"
        self.socket.sendall(option.encode('utf8'))

        # Sending client's data
        self.socket.sendall(self.name.encode('utf8'))
        self.socket.recv(1024)

        self.socket.sendall(self.psw.encode('utf8'))
        self.socket.recv(1024)

        print("Sign in data sent")

class SignUp:
    def __init__(self, frame, socket):
        self.socket = socket
        self.sgup = Button(frame, width=10, text="Sign up", activebackground='red', 
                        font=('Consolas', 11), bd=0, bg='black', fg='white', command=self.sign_up_form)
        self.sgup.place(x=138, y=320)
    
    def sign_up_form(self):
        frame = Frame(root, width=350, height=350, bg='white')
        frame.place(x=0, y=0)
        # Header title
        self.heading = Label(frame, text='Sign up', fg='#06283D',
                                bg='#DFF6FF', font=('Consolas', 19, 'bold'))
        self.heading.place(x=130, y=5)

        # Username input box
        self.user = Entry(frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Consolas', 13))
        self.user.place(x=25, y=90)
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', self.on_enter_user)
        self.user.bind('<FocusOut>', self.on_leave_user)

        # Password input box
        self.pswd = Entry(frame, width=33, fg='black', bg='#1363DF', bd=0,
                            font=('Consolas', 13))
        self.pswd.place(x=25, y=150)
        self.pswd.insert(0, 'Password')
        self.pswd.bind('<FocusIn>', self.on_enter_pswd)
        self.pswd.bind('<FocusOut>', self.on_leave_pswd)

        # Signup button
        self.btn = Button(frame, width=10, text="Sign up", activebackground='red', 
                        font=('Consolas', 11), bd=0, command=self.sign_up, bg='black', fg='white')
        self.btn.place(x=138, y=270)


    def on_enter_user(self, e):
        self.name = self.user.get()
        if self.name == 'Username':
            self.user.delete(0, 'end')
    def on_leave_user(self, e):
        self.name = self.user.get()
        if self.name == '':
            self.user.insert(0, 'Username')

    def on_enter_pswd(self, e):
        self.psw = self.pswd.get()
        if self.psw == 'Password':
            self.pswd.delete(0, 'end')
    def on_leave_pswd(self, e):
        self.psw = self.pswd.get()
        if self.psw == '':
            self.pswd.insert(0, 'Password')
    
    def sign_up(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()

        if self.name == 'Username' or self.psw == 'Password':
            print("Fields can't be empty")
            return

        # Notify server client is signing up
        option = "SIGNUP"
        self.socket.sendall(option.encode('utf8'))

        # Sending client's data
        self.socket.sendall(self.name.encode('utf8'))
        self.socket.recv(1024)

        self.socket.sendall(self.psw.encode('utf8'))
        self.socket.recv(1024)

        print("Sign up data sent")

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

signin = SignIn(root, client_socket)


root.mainloop()