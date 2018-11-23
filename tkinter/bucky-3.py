from tkinter import *

root = Tk()

# bg -> background, fg -> foreground
one = Label(root, text = "One", bg = "red", fg = "white")
one.pack()

two = Label(root, text = "Two", bg = "green", fg = "black")
two.pack(fill = X) # Will stretch in x-direction

three = Label(root, text = "Three", bg = "blue", fg = "black")
three.pack(side = LEFT, fill = Y) # Will stretch in x-direction

root.mainloop()
