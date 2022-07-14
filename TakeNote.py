from socket import *
from threading import *
from tkinter import *
import tkinter

BUFFER_SIZE = 300000
FORMAT = 'utf8'

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