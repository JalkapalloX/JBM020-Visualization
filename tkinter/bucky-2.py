from tkinter import *

root = Tk()

topFrame = Frame(root) # Invisible container in root
topFrame.pack() # Places container *somewhere*

bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM) # *somewhere* bottom

# Create button widgets
button1 = Button(topFrame, text = "Don't click!", fg = "red")
button2 = Button(topFrame, text = "Don't click!", fg = "blue")
button3 = Button(topFrame, text = "Don't click!", fg = "green")
button4 = Button(bottomFrame, text = "Don't click!", fg = "purple")

# Display button widgets
button1.pack(side = LEFT)
button2.pack(side = LEFT)
button3.pack(side = LEFT)
button4.pack(side = BOTTOM)

root.mainloop() # Infinite loop of prior lines
                # Otherwise just flashes on screen
