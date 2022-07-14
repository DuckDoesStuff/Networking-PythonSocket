from socket import *
from threading import *
from tkinter import *

FORMAT = 'utf8'

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
