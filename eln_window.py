import tkinter as tk
from tkinter import Tk, Label, Button, Scrollbar, Text, Frame

banner_height = 2
banner_width = 15
banner_bg = "light blue"
banner_fg = "black"
banner_spacer_width = 3

class eln_GUI:
    def __init__(self, master):
        self.master = master
        master.title = "ELN Main window"

        self.entryFrame = Frame(master) #set frame for text box with scrollbar
        self.testTxtBox = Text(self.entryFrame, height=10, width=100) #define textbox
        self.testTxtBox.pack(side=tk.LEFT) #pack textbox left bound
        self.scrollbar = Scrollbar(self.entryFrame) #define scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #pack scrollbar right bound

        #assign scrollbar to the respective text field
        self.scrollbar.config(command=self.testTxtBox.yview)
        self.testTxtBox.config(yscrollcommand=self.scrollbar.set)

        self.entryFrame.pack() #pack frame with text field and scrollbar

        self.label = Label(master, text="Test label")
        self.label.pack()
        
        self.btnTest = Button(master, text="Test", command= lambda: self.test(12))
        self.btnTest.pack()

        self.btnClose = Button(master, text="Close", command=master.quit)
        self.btnClose.pack()

    def test(self, number):
        print(number)

root = Tk()
gui = eln_GUI(root) #no idea what this does but it'S necessary
root.mainloop()