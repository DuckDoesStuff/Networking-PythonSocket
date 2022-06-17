import json
from ipaddress import collapse_addresses
from tkinter import *
from turtle import window_height
from urllib.parse import uses_fragment

def sayHello():
    print("Hello there")

root = Tk()
root.geometry('925x500+300+200')        #Set window size and position
root.resizable(False, False)            #Disable X and Y resizing
root.title('Testing')

class SignIn:
    def __init__(self, frame):
        frame = Frame(frame, width=350, height=350, bg='white')
        frame.place(x=0, y=0)
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
        self.label = Label(frame, text="Need an account?", font=("Consolas", 9), fg='black', bg='#1363DF', bd=0)
        self.label.place(x=122, y=295)
       

    def on_enter_user(self, e):
        self.name = self.user.get()
        if self.name == 'Username':
            self.user.delete(0, 'end')

    def on_leave_user(self, e):
        self.name = self.user.get()
        if self.name == '':
            self.user.insert(0, 'Username')
        self.unbind('<FocusOut>')

    def on_enter_pswd(self, e):
        self.psw = self.pswd.get()
        if self.psw == 'Password':
            self.pswd.delete(0, 'end')

    def on_leave_pswd(self, e):
        self.psw = self.pswd.get()
        if self.psw == '':
            self.pswd.insert(0, 'Password')
        self.unbind('<FocusOut>')           
    
    def sign_in(self):
        self.name = self.user.get()
        self.psw = self.pswd.get()
        if self.name == 'Username' or self.psw == 'Password':
            print("Fields can't be empty")
            return

        # Open and store data as a python object
        f = open('accounts.json', 'r')
        file_data = json.load(f)
        f.close()

        for i in file_data['username']:
            if i == self.name:
                for j in file_data['password']:
                    if j == self.psw:
                        print("Login successfully")
                        return
                print("Wrong password")
                return
        
        print("Username doesn't exist")

class SignUp:
    def __init__(self, frame):
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

        f = open('accounts.json', 'r+')
        file_data = json.load(f)

        for i in file_data['username']:
            if i == self.name:
                print('Username existed')
                return

        # Append new user's account to database
        file_data['username'].append(self.name)
        file_data['password'].append(self.psw)

        f.seek(0)
        json.dump(file_data, f, indent=4)

        print("Create account succesfully")
        f.close()



signin = SignIn(root)
signup = SignUp(root)


root.mainloop()