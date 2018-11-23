from tkinter import *

# ~~~~~ Main Menu ~~~~~

def doNothing():
    print("Heyaaah!!!")

root = Tk()

menu = Menu(root)
root.config(menu = menu)

subMenu = Menu(menu) # Menu structure is hierachical
menu.add_cascade(label = "File", menu = subMenu)
subMenu.add_command(label = "New Project...", command = doNothing)
subMenu.add_command(label = "New...", command = doNothing)
subMenu.add_separator() # Adds line for grouping
subMenu.add_command(label = "Exit", command = doNothing)

editMenu = Menu(menu)
menu.add_cascade(label = "Edit", menu = editMenu)
editMenu.add_command(label = "Redo", command = doNothing)

# ~~~~~ The Toolbar ~~~~~

toolbar = Frame(root, bg = "blue")
insertButton = Button(toolbar, text = "Insert Image", command = doNothing)
insertButton.pack(side = LEFT, padx = 2, pady = 2) # 2 pixels of padding (extra space)

printButton = Button(toolbar, text = "Print", command = doNothing)
printButton.pack(side = LEFT, padx = 2, pady = 2)

toolbar.pack(side = TOP, fill = X)

# ~~~~~ Status Bar ~~~~~

status = Label(root, text = "Preparing for Heyaaah!!!",
               bd = 1, relief = SUNKEN, anchor = W) # bd -> Border
                                                    # relief -> How should it appear
                                                    # W -> West

status.pack(side = BOTTOM, fill = X)

root.mainloop()
