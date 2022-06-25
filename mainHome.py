from tkinter import *

class MainHome:
    def __init__(self, frame):
        self.frame = Frame(frame, width=925, height=500, bg='red')
        self.frame.place(x=0, y=0)

root = Tk()
root.geometry('925x500+300+200')        #Set window size and position
root.resizable(False, False)            #Disable X and Y resizing
root.title('Demo')

mainHome = MainHome(root)


root.mainloop()