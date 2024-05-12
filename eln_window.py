import tkinter as tk
from tkinter import Tk, Button, Scrollbar, Text, Frame, simpledialog, messagebox, Canvas, filedialog, Toplevel, Label, Entry
import tkinter.ttk as ttk
from tkinter.ttk import Treeview
import os
import shutil
from PIL import ImageTk, Image
import PIL
from rdkit.Chem import AllChem, Draw
from eln_xml import *
import data_management
import xml.etree.ElementTree as ET
from debug import debug
import pyautogui
from tkinter.font import nametofont
import shutil

# Style Variables
banner_height = 2
banner_width = 15
banner_bg = "light blue"
banner_fg = "black"
banner_spacer_width = 3
frame_border = 5
log_height = 20
timestamp_width = 128
log_string_width = 580
info_bg = "white"
info_entry_font = ("Seoge UI", 9)
entry_width = int((log_string_width+timestamp_width)/8)
stoich_height = 9
reaction_height = 200
stoich_button_width = 27
analytics_height = 440

# Language Variables
new_entry_btn_text = "New Entry"
load_entry_btn_text = "Load Entry"
print_btn_text = "Print to PDF"
add_image_btn_text = "Attach png Image"
refresh_btn_text = "Reload File"
eln_window_title = "ELN"
timestamp_header_txt = "Timestamp"
log_string_header_txt = "Entry"
submit_btn_text = "Submit Entry"
stoich_btn_add_txt = "Add reagent"
stoich_btn_remove_txt = "Remove selected reagent"
stoich_btn_edit_txt = "Edit selected reagent"
btn_get_from_inventory_text = "Get from inventory"

class eln_window:
    def __init__(self, master):
        nametofont("TkHeadingFont").configure(family=info_entry_font[0], size=info_entry_font[1])
        nametofont("TkDefaultFont").configure(family=info_entry_font[0], size=info_entry_font[1])
        nametofont("TkDefaultFont").configure(family=info_entry_font[0], size=info_entry_font[1])
        debug("Initialization start")
        self.master = master
        self.left_frame = Frame(self.master, border=0, width=2000)
        self.right_frame = Frame(self.master, border=0, width=600)
        self.left_frame.bind("<FocusIn>", self.rootFocus)
        debug("All elements configured, packing widgets")
        # Load widgets
        self.loadBanner()
        self.loadLog()
        self.loadEntrySection()
        self.loadReactionImage()
        self.loadStoich()
        self.loadAnalytics()
        self.left_frame.pack(side=tk.LEFT)
        self.right_frame.pack(side=tk.RIGHT)

        debug("Widgets packed, initialization complete.")

    def newEntryEvent(self):
        debug("Starting new entry")
        new_entry = ""
        #code to make sure the working directory is correct
        if os.getcwd()[-4:].upper() != "\ELN":
            if os.path.exists("ELN") == False: # check if "ELN" directory exists, create if not
                os.mkdir(f"{os.getcwd()}\ELN")
            os.chdir(f"{os.path.dirname(os.path.realpath(__file__))}\ELN")
            debug("Working directory updated")
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
                debug("New entry name defined")
        if new_entry == None: # if a valid new entry is being created, copy the cdxml template from the dist folder to the new folder.
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
        else:
            debug("Copying cdxml from template")
            if not os.path.exists(f"{os.getcwd()}\\reaction.cdxml"):
                shutil.copyfile(f"{os.path.dirname(os.path.realpath(__file__))}\\template.cdxml", f"{os.getcwd()}\\reaction.cdxml")
                root = ET.Element("root")
                ET.ElementTree(root).write("log.xml")
                ET.ElementTree(root).write("stoich.xml")
                ET.ElementTree(root).write("info.xml")
                debug("Copying done")
        debug("New entry created")  

    def openChemDraw(self, event):
        debug("Trying to open CDXML file")
        try:
            os.startfile(f"{os.getcwd()}\\reaction.cdxml")
        except:
            debug("Failed to open CDXML file")
            return None
        debug("Success")

    def loadEntryEvent(self, entry_dir = None):
        debug("Start entry loading")
        if entry_dir == None:
            entry_dir = filedialog.askdirectory(mustexist=True, initialdir=f"{os.path.dirname(os.path.realpath(__file__))}\ELN")
        os.chdir(entry_dir)
        debug("Entry directory chosen")
        self.destroyLog()
        self.destroyEntrySection()
        self.loadLog()
        self.loadEntrySection()
        debug("Changed working directory, parsed log xml")
        self.updateRightFrame()
        debug("Entry loaded")

    def printEvent(self):
        debug("Printing...")

    def refreshEvent(self):
        debug("Starting window refresh")
        try:
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            root.quit()
            root.destroy()
        except: None
        debug("Window killed, restarting...")
        run()

    def attachImageEvent(self):
        debug("Attaching Image to selected entry.")
        current = self.log.focus()
        timestamp = ""
        try:
            for index, item in enumerate(self.log_items_images):
                if item[0] == current:
                    timestamp = item[1]
                    break
            else:
                return None
        except:
            debug("Could not find selected entry.")
            return None
        file = filedialog.askopenfilename(filetypes=[("PNG Image Files", "*.png")])
        print(file)
        print(f"{os.getcwd()}\{timestamp.replace(':', '_')}.png".replace("\\", "/"))
        shutil.copyfile(src=file, dst=f"{os.getcwd()}\{timestamp.replace(':', '_')}.png".replace("\\", "/"))

    def submitEvent(self):
        debug("Submitting Entry")
        entry_text = self.entry_field.get("1.0",'end-1c')
        if addEntry(entry_text) == True:
            self.destroyLog()
            self.destroyEntrySection()
            self.loadLog()
            self.loadEntrySection()
            debug("Finished submitting entry")
        else:
            debug("Failed to submit entry")  

    def destroyBanner(self):
        debug("Destroying button banner")
        try:
            self.left_spacer.destroy()
            self.new_entry_button.destroy()
            self.new_entry_spacer.destroy()
            self.load_entry_button.destroy()
            self.load_entry_spacer.destroy()
            self.print_button.destroy()
            self.print_spacer.destroy()
            self.refresh_button.destroy()
            self.refresh_spacer.destroy()
            self.add_image_button.destroy()
            self.banner_frame.destroy()
        except:
            debug("Failed to destroy button banner")
            return None
        debug("Done")

    def loadBanner(self):
        debug("Loading button banner")
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
        self.add_image_button = Button(text=add_image_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=self.banner_frame, command=self.attachImageEvent)

        self.left_spacer.pack(side=tk.LEFT)
        self.new_entry_button.pack(side=tk.LEFT)
        self.new_entry_spacer.pack(side=tk.LEFT)
        self.load_entry_button.pack(side=tk.LEFT)
        self.load_entry_spacer.pack(side=tk.LEFT)
        self.print_button.pack(side=tk.LEFT)
        self.print_spacer.pack(side=tk.LEFT)
        self.refresh_button.pack(side=tk.LEFT)
        self.refresh_spacer.pack(side=tk.LEFT)
        self.add_image_button.pack(side=tk.LEFT)
        self.banner_frame.pack(anchor="nw")
        debug("Done")

    def destroyLog(self):
        debug("Destroying log")
        try:
            self.entry_field.delete("1.0", tk.END)
            self.log.destroy()
            self.log_scroll.destroy()
            self.log_frame.destroy()
        except:
            debug("Failed to destroy log")
            return None
        debug("Done")

    def loadLog(self): #code for loading the log table
        debug("Loading Log")
        style = ttk.Style(root)
        style.configure("log.Treeview", rowheight=40)
        self.log_frame = Frame(self.left_frame, border=frame_border)
        self.log = Treeview(self.log_frame, columns=("timestamp", "log_string"), show="headings", height=log_height, style="log.Treeview")
        self.log_scroll = Scrollbar(self.log_frame)

        self.log.column("#0", width=41)
        self.log.heading("timestamp", text=timestamp_header_txt)
        self.log.column("timestamp", width=timestamp_width, stretch=False)
        self.log.heading("log_string", text=log_string_header_txt)
        self.log.column("log_string", width=log_string_width, stretch=False)
        entries = readEntries()
        log_items = []
        for entry, _ in enumerate(entries):
            log_display = entries[entry][0], entries[entry][1]
            log_items.append((self.log.insert('', tk.END, values=log_display), entries[entry][0]))

        self.log_items_images = self.loadLogImages(log_items)
        
        self.log.pack(side=tk.LEFT)
        self.log.bind("<ButtonRelease-1>", self.displayLogImage)
        self.log_scroll.pack(side=tk.RIGHT, fill = tk.Y)
        self.log_scroll.config(command=self.log.yview)
        self.log.config(yscrollcommand=self.log_scroll.set)
        self.log_frame.pack()
        debug("Done")

    def displayLogImage(self, event):
        current = self.log.focus()
        debug(f"{current} selected.")
        for index, items in enumerate(self.log_items_images):
            if items[0] == current:
                self.destroyAnalytics()
                self.loadAnalytics(items[2])

    def loadLogImages(self, log_items): # takes a list of tuples containing a treeview row item and a timestamp and returns the same structure with an image object attached if an image with the same name as the timestamp exists in the working directory
        try:
            log_items_images = []
            for index, log_item in enumerate(log_items):
                image_name_fn = log_item[1].replace(":", "_")
                debug(f"Checking for image {image_name_fn}.png")
                if os.path.isfile(f"{image_name_fn}.png"):
                    debug(f"{image_name_fn}.png exists, loading...")
                    with Image.open(f"{image_name_fn}.png") as image:
                        tkimage = ImageTk.PhotoImage(image)
                        log_items_images.append((log_item[0], log_item[1], tkimage))
                else:
                    debug(f"{image_name_fn}.png does not exist...")
                    log_items_images.append((log_item[0], log_item[1], None))
            return log_items_images
        except:
            return None

    def destroyEntrySection(self):
        debug("Destroying entry section")
        try:
            self.entry_field.destroy()
            self.entry_frame.destroy()
            self.entry_spacer.destroy()
        except:
            debug("Failed to destroy entry section")
            return None
        debug("Done")

    def loadEntrySection(self):
        debug("Loading entry section")
        self.entry_frame = Frame(self.left_frame, border=frame_border)
        self.entry_field = Text(self.entry_frame, background=info_bg, font=info_entry_font, width=entry_width, height=2)
        self.entry_spacer = Frame(self.entry_frame, width=banner_spacer_width, height=banner_height)
        self.submit_entry_button = Button(self.entry_frame, text=submit_btn_text, width=14, height=banner_height, bg=banner_bg, fg=banner_fg, command=self.submitEvent)
        self.entry_field.pack(side=tk.LEFT)
        self.entry_spacer.pack(side=tk.LEFT)
        self.submit_entry_button.pack(side=tk.RIGHT, fill=tk.X)
        self.entry_frame.pack(anchor="w")
        debug("Done")

    def destroyReactionImage(self):
        debug("Destroying reaction image canvas")
        try:
            self.reaction_image_frame.destroy()
            self.reaction_image.destroy()
        except:
            debug("Failed to destroy reaction image canvas")
            return None
        debug("Done")

    def loadReactionImage(self):
        debug("Loading reaction image canvas")
        self.reaction_image_frame = Frame(self.right_frame, height=reaction_height, width=600, border=frame_border)
        self.reaction_image_frame.bind("<FocusIn>", self.rootFocus)
        self.reaction_image = Canvas(self.reaction_image_frame, height=reaction_height, width=600, background="white")
        try:
            m = AllChem.ReactionsFromCDXMLFile("reaction.cdxml")
            debug("Parsed cdxml file")
            nReactants = m[0].GetNumReactantTemplates() + m[0].GetNumAgentTemplates()*1.3 + m[0].GetNumProductTemplates()
            debug(f"Image width modifier: {nReactants}")
            img = Draw.ReactionToImage(m[0], subImgSize=(int(800/(nReactants*1)), reaction_height))
            ratio = img.size[0]/img.size[1]
            debug("Converted reaction to image")
            img = img.resize((600, int(600/ratio)), resample=PIL.Image.LANCZOS)
            if img.size[1] > reaction_height:
                img = img.resize((int(reaction_height*ratio), reaction_height), resample=PIL.Image.LANCZOS)
            debug("Rescaled image")
            self.imgtk = ImageTk.PhotoImage(img)
            debug("Converted to TKInter compatible format")
        except:
            debug("Could not load image")
            self.reaction_image.pack()
            self.reaction_image.bind("<Double-1>", self.openChemDraw)
            self.reaction_image_frame.pack(side=tk.TOP)
            return None

        self.reaction_image.bind("<Double-1>", self.openChemDraw)
        self.reaction_image.create_image((0,0), anchor=tk.NW, image=self.imgtk)
        self.reaction_image.pack(side=tk.TOP)
        self.reaction_image_frame.pack(side=tk.TOP)
        debug("Done")
        
    def destroyStoich(self):
        debug("Destroying stoichiometry table")
        try:
            for child in self.right_frame.winfo_children():
                child.destroy()
        except:
            debug("Failed to destroy stoichiometry table")
            return None
        debug("Done")

    def loadStoich(self):
        debug("Loading stoichiometry table")
        self.stoich_frame = Frame(self.right_frame, height=200, width=600, border=frame_border)
        self.stoich_table = Treeview(self.stoich_frame, columns=("ID", "Substance", "M", "n", "m", "V", "eq.", "notes"), show="headings", height=stoich_height)
        self.stoich_button_frame = Frame(self.stoich_frame)
        self.stoich_button_add = Button(self.stoich_button_frame, text=stoich_btn_add_txt, width=stoich_button_width, height=2, bg=banner_bg, fg=banner_fg, command=self.stoichAddEvent)
        self.stoich_button_edit = Button(self.stoich_button_frame, text=stoich_btn_edit_txt, width=stoich_button_width, height=2, bg=banner_bg, fg=banner_fg, command=self.stoichEditEvent)
        self.stoich_button_remove = Button(self.stoich_button_frame, text=stoich_btn_remove_txt, width=stoich_button_width, height=2, bg=banner_bg, fg=banner_fg, command=self.stoichRemoveEvent)
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

        entries = readStoich()
        try:
            for entry, _ in enumerate(entries):
                stoich_table_display = entries[entry][0], entries[entry][1], entries[entry][2], entries[entry][3], entries[entry][4], entries[entry][5], entries[entry][6], entries[entry][7]
                self.stoich_table.insert('', tk.END, values=stoich_table_display)
        except: None
        self.stoich_table.pack()
        self.stoich_button_add.pack(side=tk.LEFT)
        self.stoich_button_edit.pack(side=tk.LEFT)
        self.stoich_button_remove.pack(side=tk.LEFT)
        self.stoich_button_frame.pack()
        self.stoich_frame.pack()
        debug("Done")

    def destroyAnalytics(self):
        debug("Destroying analytics section")
        try:
            self.analytics_frame.destroy()
            self.analytics_scrolly.destroy()
        except:
            debug("Failed to destroy analytics section")
            return None

    def loadAnalytics(self, analytics_image = None):# analytics section TODO
        debug("Loading Analytics section")
        self.analytics_frame = Frame(self.right_frame, height=analytics_height, width=600, border=0, padx=0, pady=0, background="white")
        self.analytics_scrollx = Scrollbar(self.analytics_frame, orient="horizontal")
        self.analytics_scrolly = Scrollbar(self.analytics_frame)
        if analytics_image != None:
            self.analytics_image = Canvas(self.analytics_frame, height=analytics_height, width=600, background="white", scrollregion=(0,0,analytics_image.width(),analytics_image.height()))
            self.analytics_image.create_image((int(analytics_image.width()/2),int(analytics_image.height()/2)), anchor=tk.CENTER, image=analytics_image)
        else:
            self.analytics_image = Canvas(self.analytics_frame, height=analytics_height, width=600, background="white", scrollregion=(0,0,0,0))
        self.analytics_scrollx.pack(side=tk.BOTTOM, fill = tk.X)
        self.analytics_scrollx.config(command=self.analytics_image.xview)
        self.analytics_scrolly.pack(side=tk.RIGHT, fill = tk.Y)
        self.analytics_scrolly.config(command=self.analytics_image.yview)
        self.analytics_image.config(xscrollcommand=self.analytics_scrollx.set,yscrollcommand=self.analytics_scrolly.set)
        self.analytics_frame.bind("<FocusIn>", self.rootFocus)
        self.analytics_image.pack(side=tk.LEFT)
        self.analytics_frame.pack()
        debug("Done")

    def rootFocus(self, event):
        self.updateRightFrame()
        return None
    
    def updateRightFrame(self):
        self.destroyReactionImage()
        self.destroyStoich()
        self.destroyAnalytics()
        self.loadReactionImage()
        self.loadStoich()
        self.loadAnalytics()
    
    def stoichAddEvent(self):
        debug("Adding entry to stoichiometry table")
        self.stoich_add_window = Toplevel(self.right_frame)
        self.stoich_add_window.title("Add new reagent")
        mousepos = pyautogui.position()
        self.stoich_add_window.geometry(f"+{mousepos[0]-45}+{mousepos[1]-45}")
        self.stoich_add_window.resizable(width=False, height=False)
        self.stoich_add_window.attributes('-topmost', True)
        self.loadStoichWindowLayout("add")
    
    def stoichRemoveEvent(self):
        current_id = self.stoich_table.item(self.stoich_table.selection())["values"][0]
        current_name = self.stoich_table.item(self.stoich_table.selection())["values"][1]
        debug(f"Removing entry {current_id} ({current_name}) from stoichiometry table")
        deleteStoich(current_id)
        self.updateRightFrame()

    def stoichEditEvent(self):
        debug("Editing entry in stoichiometry table")
        try:
            self.stoich_table.item(self.stoich_table.selection())["values"][0]
        except:
            messagebox.showerror("No Item Selected", "No item from the stoichiometry table was selected.")
            return None
        self.stoich_edit_window = Toplevel()
        self.stoich_edit_window.title("Edit reagent data")
        mousepos = pyautogui.position()
        self.stoich_edit_window.geometry(f"+{mousepos[0]-45}+{mousepos[1]-45}")
        self.stoich_edit_window.resizable(width=False, height=False)
        self.stoich_edit_window.attributes('-topmost', True)
        self.loadStoichWindowLayout("edit")

    def loadStoichWindowLayout(self, master):
        if master == "add":
            self.stoich_frame = Frame(master=self.stoich_add_window, background=info_bg)
        else:
            self.stoich_frame = Frame(master=self.stoich_edit_window, background=info_bg)
        self.stoich_label_frame = Frame(border=5, master=self.stoich_frame, background=info_bg)
        self.id_label = Label(text="ID", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)
        self.name_label = Label(text="Substance", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)
        self.M_label = Label(text="M [g/mol]", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)
        self.n_label = Label(text="n [mol]", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)
        self.m_label = Label(text="m [g]", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)
        self.V_label = Label(text="V [ml]", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)
        self.eq_label = Label(text="eq.", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)
        self.notes_label = Label(text="Notes", master=self.stoich_label_frame, background=info_bg, font=info_entry_font)

        self.stoich_entry_frame = Frame(border=5, master=self.stoich_frame, background=info_bg)
        self.id_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)
        self.name_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)
        self.M_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)
        self.n_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)
        self.m_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)
        self.V_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)
        self.eq_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)
        self.notes_entry = Entry(master=self.stoich_entry_frame, background=info_bg, font=info_entry_font, width=10, border=2)

        if not master == "add":
            current_id = self.stoich_table.item(self.stoich_table.selection())["values"][0]
            current_entry_raw = readStoichSingle(current_id)
            print(current_entry_raw)
            current_entry = []
            for item in current_entry_raw: #replaces all None Type elements with ""
                if type(item) is not str:
                    current_entry.append("")
                else:
                    current_entry.append(item)
            print(current_entry)
            self.id_entry.insert(0, current_id)
            self.name_entry.insert(0, current_entry[0])
            self.M_entry.insert(0, current_entry[1])
            self.n_entry.insert(0, current_entry[2])
            self.m_entry.insert(0, current_entry[3])
            self.V_entry.insert(0, current_entry[4])
            self.eq_entry.insert(0, current_entry[5])
            self.notes_entry.insert(0, current_entry[6])

        button_text = None
        if master == "add":
            self.get_from_inventory = tk.Button(master=self.stoich_add_window, background=banner_bg, foreground=banner_fg, text=btn_get_from_inventory_text, width=22, pady=10, command=self.getFromInventoryEvent)
            self.get_from_inventory.pack(side=tk.TOP)
            button_text = "Add substance entry"
            self.save_stoich_entry_spacer = tk.Frame(master=self.stoich_add_window, height=5)
            self.save_stoich_entry_button = tk.Button(master=self.stoich_add_window, background=banner_bg, foreground=banner_fg, text=button_text, width=22, pady=10, command=self.addStoichEntryEvent)
        else:
            self.save_stoich_entry_spacer = tk.Frame(master=self.stoich_edit_window, height=5)
            button_text = "Edit substance entry"
            self.save_stoich_entry_button = tk.Button(master=self.stoich_edit_window, background=banner_bg, foreground=banner_fg, text=button_text, width=22, pady=10, command=self.editStoichEntryEvent)
        
        self.id_label.pack(anchor="e")
        self.name_label.pack(anchor="e")
        self.M_label.pack(anchor="e")
        self.n_label.pack(anchor="e")
        self.m_label.pack(anchor="e")
        self.V_label.pack(anchor="e")
        self.eq_label.pack(anchor="e")
        self.notes_label.pack(anchor="e")

        self.id_entry.pack()
        self.name_entry.pack()
        self.M_entry.pack()
        self.n_entry.pack()
        self.m_entry.pack()
        self.V_entry.pack()
        self.eq_entry.pack()
        self.notes_entry.pack()
        self.stoich_label_frame.pack(side=tk.LEFT)
        self.stoich_entry_frame.pack(side=tk.LEFT)
        self.save_stoich_entry_button.pack(side=tk.BOTTOM)
        self.save_stoich_entry_spacer.pack(side=tk.BOTTOM)
        self.stoich_frame.pack()
        
        return None

    def getFromInventoryEvent(self):
        debug("Getting data from inventory")
        inv_id = simpledialog.askstring("Provide ID", "Please provide the ID of the substance you want to use in this entry:")
        if inv_id != None:
            try:
                data = data_management.readEntry(inv_id)
                debug(f"Fetched data: {data}")
                self.id_entry.insert(0, data[0])
                self.name_entry.insert(0, data[1])
                self.M_entry.insert(0, data[8][:-6]) # removes g/mol unit
            except:
                debug("Could not load from inventory. Does the provided ID exist?")
                return None
        else:
            debug("No valid ID was provided.")

    def addStoichEntryEvent(self):
        addStoich(id=self.id_entry.get(),
                name=self.name_entry.get(),
                M=self.M_entry.get(),
                n=self.n_entry.get(),
                m=self.m_entry.get(),
                V=self.V_entry.get(),
                eq=self.eq_entry.get(),
                notes=self.notes_entry.get(),)
        self.stoich_add_window.destroy()
        self.updateRightFrame()
        return None
    
    def editStoichEntryEvent(self):
        editStoich(id=self.id_entry.get(),
                chem_name=self.name_entry.get(),
                M=self.M_entry.get(),
                n=self.n_entry.get(),
                m=self.m_entry.get(),
                V=self.V_entry.get(),
                eq=self.eq_entry.get(),
                notes=self.notes_entry.get())
        self.stoich_edit_window.destroy()
        self.updateRightFrame()
        return None
    
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