from tkinter import *

root = Tk()

def printName():
    print("Heyaaah!")

button1 = Button(root, text = "Let's go", command = printName)
button1.pack()

root.mainloop()
