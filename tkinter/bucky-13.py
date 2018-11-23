from tkinter import *

root = Tk()

photo = PhotoImage(file = "Untitled.png")
label = Label(root, image = photo)
label.pack()

root.mainloop()
