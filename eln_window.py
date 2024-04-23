import tkinter as tk
from tkinter import Tk, Button, Scrollbar, Text, Frame, simpledialog, messagebox, Canvas, filedialog
from tkinter.ttk import Treeview
import os
import shutil
from PIL import ImageTk
import PIL
from rdkit.Chem import AllChem, Draw
from eln_xml import addEntry, readEntries
import xml.etree.ElementTree as ET
import time

global debug_print, ref_time
debug_print = True
ref_time = round(time.time() * 1000) #time in micros at program start

def debug(text): #debug break points (only if enabled)
    global debug_print, ref_time
    if debug_print == True:
        current_time = round(time.time() * 1000)
        print(f"Time since last debug call: {current_time-ref_time} ms, Debug Message: {text}")
        ref_time = current_time

# Style Variables
banner_height = 2
banner_width = 15
banner_bg = "light blue"
banner_fg = "black"
banner_spacer_width = 3
frame_border = 5
log_height = 25
timestamp_width = 112
log_string_width = 600
info_bg = "white"
info_entry_font = ("Seoge UI", 11)
entry_width = int(log_string_width/8)
stoich_height = 9

# Language Variables
new_entry_btn_text = "New Entry"
load_entry_btn_text = "Load Entry"
print_btn_text = "Print to PDF"
close_btn_text = "Save and Exit"
refresh_btn_text = "Reload File"
eln_window_title = "ELN"
timestamp_header_txt = "Timestamp"
log_string_header_txt = "Entry"
submit_btn_text = "Submit Entry"


class eln_window:
    def __init__(self, master):
        self.master = master
        # Initialize the left hand frame containing the button header, log, entry field and submission button
        self.left_frame = Frame(self.master, border=0)
        self.right_frame = Frame(self.master, border=0, width=600)
        # Button banner init
        self.banner_frame = Frame(self.left_frame, border=frame_border)
        self.left_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.new_entry_button = Button(text=new_entry_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.newEntryEvent)
        self.new_entry_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.load_entry_button = Button(text=load_entry_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.loadEntryEvent)
        self.load_entry_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.print_button = Button(text=print_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.printEvent)
        self.print_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
        self.refresh_button = Button(text=refresh_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.refreshEvent)
        self.refresh_spacer = Frame(width=banner_spacer_width, height=banner_height, master=self.banner_frame)
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
        self.submit_entry_button = Button(self.entry_frame, text=submit_btn_text, width=12, height=banner_height, bg=banner_bg, fg=banner_fg, command=self.submitEvent)
        # reaction image canvas init
        self.reaction_image_frame = Frame(self.right_frame, height=200, width=600, border=frame_border)
        self.reaction_image = Canvas(self.reaction_image_frame, height=200, width=600, background="white")
        # stoichiometry table init
        self.stoich_frame = Frame(self.right_frame, height=200, width=600, border=frame_border)
        self.stoich_table = Treeview(self.stoich_frame, columns=("ID", "Substance", "M", "n", "m", "V", "eq.", "notes"), show="headings", height=stoich_height)
        # stoich table style:
        self.stoich_table.heading("ID", text="ID")
        self.stoich_table.heading("Substance", text="Substance")
        self.stoich_table.heading("M", text="M [g/mol]")
        self.stoich_table.heading("n", text="n [mol]")
        self.stoich_table.heading("m", text="m [g]")
        self.stoich_table.heading("V", text="V [mL]")
        self.stoich_table.heading("eq.", text="eq.")
        self.stoich_table.heading("notes", text="Notes")
        self.stoich_table.column("ID", width=35, stretch=False)
        self.stoich_table.column("Substance", width=200, stretch=False)
        self.stoich_table.column("M", width=65, stretch=False)
        self.stoich_table.column("n", width=47, stretch=False)
        self.stoich_table.column("m", width=42, stretch=False)
        self.stoich_table.column("V", width=42, stretch=False)
        self.stoich_table.column("eq.", width=35, stretch=False)
        self.stoich_table.column("notes", width=135, stretch=False)
        # analytics section TODO
        self.analytics_frame = Frame(self.right_frame, height=210, width=600, border=frame_border, background="white")

        # Pack widgets in suitable order
        # Button header/banner
        self.left_spacer.pack(side=tk.LEFT)
        self.new_entry_button.pack(side=tk.LEFT)
        self.new_entry_spacer.pack(side=tk.LEFT)
        self.load_entry_button.pack(side=tk.LEFT)
        self.load_entry_spacer.pack(side=tk.LEFT)
        self.print_button.pack(side=tk.LEFT)
        self.print_spacer.pack(side=tk.LEFT)
        self.refresh_button.pack(side=tk.LEFT)
        self.refresh_spacer.pack(side=tk.LEFT)
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
        # image canvas
        self.reaction_image.pack()
        self.reaction_image_frame.pack(side=tk.TOP)
        # stoich
        self.stoich_table.pack(side=tk.LEFT)
        self.stoich_frame.pack()
        # analytics TODO
        self.analytics_frame.pack()

    def newEntryEvent(self):
        new_entry = ""
        #code to make sure the working directory is correct
        if os.getcwd()[-4:].upper() != "\ELN":
            if os.path.exists("ELN") == False: # check if "ELN" directory exists, create if not
                os.mkdir(f"{os.getcwd()}\ELN")
            os.chdir(f"{os.path.dirname(os.path.realpath(__file__))}\ELN")
            while True:
                new_entry = simpledialog.askstring("Entry Name", "Please provide a unique Name for your journal entry:") # ask for the new entry name, make a folder with said name
                if new_entry != "" and os.path.exists(new_entry) == False: # check if entry directory exists, create if not, raise error if it already exists
                    os.mkdir(f"{os.getcwd()}\{new_entry}")
                    os.chdir(f"{os.getcwd()}\{new_entry}")
                    break
                elif new_entry != None:
                    messagebox.showerror(title="Entry invalid", message="The Entry you are trying to create already exists or is invalid.")
                    new_entry = ""
                else:
                    return None
        if new_entry == None: # if a valid new entry is being created, copy the cdxml template from the dist folder to the new folder.
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
        else:
            if not os.path.exists(f"{os.getcwd()}\\reaction.cdxml"):
                shutil.copyfile(f"{os.path.dirname(os.path.realpath(__file__))}\\template.cdxml", f"{os.getcwd()}\\reaction.cdxml")
                root = ET.Element("root")
                ET.ElementTree(root).write("log.xml")
                os.startfile(f"{os.getcwd()}\\reaction.cdxml") # opens the file in chemdraw, this is just for testing purposes for now.
        

    def loadEntryEvent(self, entry_dir = None):
        debug("Start entry loading")
        if entry_dir == None:
            entry_dir = filedialog.askdirectory(mustexist=True, initialdir=f"{os.path.dirname(os.path.realpath(__file__))}\ELN")
        debug("Entry directory chosen")
        #test code for displaying a chemdraw file as image
        os.chdir(entry_dir)
        self.loadLog()
        debug("Changed working directory, parsed log xml")
        m = AllChem.ReactionsFromCDXMLFile("reaction.cdxml")
        debug("parsed cdxml file")
        nReactants = m[0].GetNumReactantTemplates() + m[0].GetNumAgentTemplates()*1.3 + m[0].GetNumProductTemplates()
        debug(f"image width modifier: {nReactants}")
        img = Draw.ReactionToImage(m[0], subImgSize=(int(800/(nReactants*1)), 200))
        ratio = img.size[0]/img.size[1]
        debug("converted reaction to image")
        img = img.resize((600, int(600/ratio)), resample=PIL.Image.LANCZOS)
        if img.size[1] > 200:
            img = img.resize((int(200*ratio), 200), resample=PIL.Image.LANCZOS)
        debug("rescaled image")
        self.imgtk = ImageTk.PhotoImage(img)
        debug("converted to TKInter compatible format")
        self.reaction_image.destroy()
        self.reaction_image = Canvas(self.reaction_image_frame, height=200, width=600, background="white")
        self.reaction_image.create_image((0,0), anchor=tk.NW, image=self.imgtk)
        debug("set image display")
        self.reaction_image.pack()

    def printEvent(self):
        print("Print")

    def refreshEvent(self):
        try:
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            root.quit()
            root.destroy()
        except: None
        run()


    def closeEvent(self):
        print("Close")
        try:
            root.quit()
            root.destroy()
        except: None

    def submitEvent(self):
        if addEntry(self.entry_field.get("1.0",'end-1c')) == True:
            self.loadLog()
            
    def loadLog(self):
        self.entry_field.delete("1.0", tk.END)
        self.log.destroy()
        self.log_scroll.destroy()
        self.log_frame.destroy()
        # log init
        self.log_frame = Frame(self.left_frame, border=frame_border)
        self.log = Treeview(self.log_frame, columns=("timestamp", "log_string"), show="headings", height=log_height)
        self.log_scroll = Scrollbar(self.log_frame)
        # log table style
        self.log.heading("timestamp", text=timestamp_header_txt)
        self.log.column("timestamp", width=timestamp_width, stretch=False)
        self.log.heading("log_string", text=log_string_header_txt)
        self.log.column("log_string", width=log_string_width, stretch=False)
        entries = readEntries()
        for entry, _ in enumerate(entries):
            log_display = entries[entry][0], entries[entry][1]
            self.log.insert('', tk.END, values=log_display)
        self.log.pack(side=tk.LEFT)
        self.log_scroll.pack(side=tk.RIGHT, fill = tk.Y)
        self.log_scroll.config(command=self.log.yview)
        self.log.config(yscrollcommand=self.log_scroll.set)
        self.log_frame.pack()
        # entry field init
        self.entry_field.destroy()
        self.entry_frame.destroy()
        self.entry_spacer.destroy()
        self.entry_frame = Frame(self.left_frame, border=frame_border)
        self.entry_field = Text(self.entry_frame, background=info_bg, font=info_entry_font, width=entry_width, height=2)
        self.entry_spacer = Frame(self.entry_frame, width=banner_spacer_width, height=banner_height)
        self.submit_entry_button = Button(self.entry_frame, text=submit_btn_text, width=12, height=banner_height, bg=banner_bg, fg=banner_fg, command=self.submitEvent)
        self.entry_field.pack(side=tk.LEFT)
        self.entry_spacer.pack(side=tk.LEFT)
        self.submit_entry_button.pack(side=tk.RIGHT, fill=tk.X)
        self.entry_frame.pack(anchor="w")


def run():
    global root
    root = Tk()
    root.title(eln_window_title)
    root.iconbitmap("icon.ico")
    root.geometry("+10+10")
    root.resizable(width=False, height=False)
    eln_window(root) #no idea what this does but it's necessary
    root.mainloop()

run()