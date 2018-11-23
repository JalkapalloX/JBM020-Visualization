from tkinter import *

root = Tk()

# Create widgets
label1 = Label(root, text = "Name")
label2 = Label(root, text = "Password")

entry1 = Entry() # Blank field for user input
entry2 = Entry()

# Organize widgets
label1.grid(row = 0, sticky = E) # default: column = 0
                                 # E -> East: Right
label2.grid(row = 1, sticky = E)

entry1.grid(row = 0, column = 1)
entry2.grid(row = 1, column = 1)

# Checkbox
c = Checkbutton(root, text = "keep me logged in")
c.grid(columnspan = 2)

root.mainloop()
