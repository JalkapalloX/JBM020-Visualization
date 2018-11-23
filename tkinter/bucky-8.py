from tkinter import *

class BuckysButtons:
    # Initialize
    def __init__(self, master): # Master is main window
        frame = Frame(master) # Invisibe container
        frame.pack()

        self.printButton = Button(frame, text = "Print Message", command = self.printMessage)
        self.printButton.pack(side = LEFT)

        self.quitButton = Button(frame, text = "Quit", command = master.destroy)
        self.quitButton.pack(side = LEFT)

    def printMessage(self):
        print("Wow, this actually worked!")

root = Tk()
b = BuckysButtons(root)
root.mainloop()
