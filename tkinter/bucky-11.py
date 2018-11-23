from tkinter import *
import tkinter.messagebox

root = Tk()

tkinter.messagebox.showinfo("Window Title", "Heyaaaahh!!")

answer = tkinter.messagebox.askquestion("Question 1", "Heyaaahhh??")
if answer == "yes":
    print("xD")

root.mainloop()
