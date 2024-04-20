import tkinter as tk
from tkinter import Tk, Button, Scrollbar, Text, Frame, Entry
from tkinter.ttk import Treeview

# Style Variables
banner_height = 2
banner_width = 15
banner_bg = "light blue"
banner_fg = "black"
banner_spacer_width = 3
frame_border = 5
log_height = 30
timestamp_width = 100
log_string_width = 700
info_bg = "white"
info_entry_font = ("Seoge UI", 11)
entry_width = int(log_string_width/8)

# Language Variables
new_entry_btn_text = "New Entry"
load_entry_btn_text = "Load Entry"
print_btn_text = "Print to PDF"
close_btn_text = "Save and Exit"
eln_window_title = "ELN"
timestamp_header_txt = "Timestamp"
log_string_header_txt = "Entry"
submit_btn_text = "Submit Entry"
class eln_window:
    def __init__(self, master):
        self.master = master
        # Initialize the left hand frame containing the button header, log, entry field and submission button
        self.left_frame = Frame(self.master, border=frame_border)
        self.right_frame = Frame(self.master, border=frame_border)
        # Button banner init
        self.banner_frame = Frame(self.left_frame, border=frame_border)
        self.left_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.new_entry_button = Button(text=new_entry_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.newEntryEvent)
        self.new_entry_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.load_entry_button = Button(text=load_entry_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.loadEntryEvent)
        self.load_entry_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.print_button = Button(text=print_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.printEvent)
        self.print_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.close_button = Button(text=close_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.closeEvent)
        # log init
        self.log_frame = Frame(self.left_frame, border=frame_border)
        self.log = Treeview(self.log_frame, columns=("timestamp", "log_string"), show="headings", height=log_height)
        self.log_scroll = Scrollbar(self.log_frame)
        # log table style
        self.log.heading("timestamp", text=timestamp_header_txt)
        self.log.column("timestamp", width=timestamp_width, stretch=False)
        self.log.heading("log_string", text=log_string_header_txt)
        self.log.column("log_string", width=log_string_width, stretch=False)
        # entry field init
        self.entry_frame = Frame(self.left_frame, border=frame_border)
        self.entry_field = Text(self.entry_frame, background=info_bg, font=info_entry_font, width=entry_width, height=2)
        self.entry_spacer = Frame(self.entry_frame, width=banner_spacer_width, height=banner_height)
        self.submit_entry_button = Button(self.entry_frame, text=submit_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, command=self.submitEvent)

        # Pack widgets in suitable order
        # Button header/banner
        self.left_spacer.pack(side=tk.LEFT)
        self.new_entry_button.pack(side=tk.LEFT)
        self.new_entry_spacer.pack(side=tk.LEFT)
        self.load_entry_button.pack(side=tk.LEFT)
        self.load_entry_spacer.pack(side=tk.LEFT)
        self.print_button.pack(side=tk.LEFT)
        self.print_spacer.pack(side=tk.LEFT)
        self.close_button.pack(side=tk.LEFT)
        self.banner_frame.pack(anchor="nw")
        # log table
        self.log.pack(side=tk.LEFT)
        self.log_scroll.pack(side=tk.RIGHT, fill = tk.Y)
        self.log_scroll.config(command=self.log.yview)
        self.log.config(yscrollcommand=self.log_scroll.set)
        self.log_frame.pack()
        # main frames
        self.left_frame.pack(side=tk.LEFT)
        self.right_frame.pack(side=tk.RIGHT)
        # entry field
        self.entry_field.pack(side=tk.LEFT)
        self.entry_spacer.pack(side=tk.LEFT)
        self.submit_entry_button.pack(side=tk.RIGHT, fill=tk.X)
        self.entry_frame.pack(anchor="w")

    def newEntryEvent(self):
        print("New Entry")

    def loadEntryEvent(self):
        print("Load Entry")

    def printEvent(self):
        print("Print")

    def closeEvent(self):
        print("Close")
        self.master.quit()

    def submitEvent(self):
        print("Submit Entry")

root = Tk()
root.title(eln_window_title)
root.iconbitmap("icon.ico")
gui = eln_window(root) #no idea what this does but it's necessary
root.mainloop()