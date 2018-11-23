from tkinter import *

root = Tk()

def printName(event):
    print("Heyaaah!")

button1 = Button(root, text = "Let's go")
button1.bind("<Button-1>", printName) # Button1 is Left Mouse
button1.pack()

root.mainloop()
