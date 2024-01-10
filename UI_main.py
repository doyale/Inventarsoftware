import sys, os
if sys.executable.endswith('pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.path.join(os.getenv('TEMP'), 'stderr-{}'.format(os.path.basename(sys.argv[0]))), "w")
    
"""
Resources used:
https://realpython.com/python-gui-tkinter/
https://www.pythontutorial.net/tkinter/tkinter-treeview/
"""


import tkinter as tk
import tkinter.messagebox as popup
from tkinter import ttk
from data_management import readEntries, editEntry, readEntry, deleteEntry
from query import dbQuery
import tkinter.simpledialog as dialog
from new_entry_window import newEntry

#style variables
banner_height = 2
banner_width = 15
banner_bg = "light blue"
banner_fg = "black"
banner_spacer_width = 3
db_table_column_width = 140
db_table_column_width = (50, 250, 120, 70, 100, 80, 120)
info_bg = "white"
db_table_height = 51
info_entry_font = ("Seoge UI", 11)
entry_width = 53
entry_height = 10
info_spacer_height = 153
spacer_dimensions = 18

#language specific variables
new_entry_btn_text = "New Entry"
query_btn_text = "Query"
refresh_btn_text = "Refresh Table"
print_label_btn_text = "Print"
delete_entry_btn_text = "Delete entry"
db_window_title = "Chemical Database"
db_table_header_titles = ("ID", "Name", "CAS-No.", "Quantity", "Supplier", "Date received", "Storage location")
db_table_headers = ("db_id", "db_name", "db_cas", "db_qty", "db_supplier", "db_date", "db_location")
id_title_name = "ID: "
name_title_name = "Name: "
cas_title_name = "Cas No.: "
formula_title_name = "Sum formula: "
qty_title_name = "Quantity: "
purity_title_name = "Purity: "
supplier_title_name = "Supplier: "
date_title_name = "Date received: "
mass_title_name = "Molar mass: "
mp_title_name = "Melting Point: "
bp_title_name = "Boiling Point: "
density_title_name = "Density: "
location_title_name = "Storage Location: "
haz_title_name = "Hazard statements: "
prec_title_name = "Precautionary statements: "
ghs_title_name = "GHS Symbols: "
misc_title_name = "Additional info: "
edit_btn_text = "Edit selected entry"



#other variables

#command functions:
def newEntryEvent():
    global db_table
    global db_table_frame
    newEntry()

def query():
    global db_table
    global db_table_frame
    input = dialog.askstring("Query", "Please enter your search term:")
    db_table.destroy()
    db_table_frame.destroy()
    db_table, db_table_frame = initTable("query", input)

def refresh():
    global db_table
    global db_table_frame
    db_table.destroy()
    db_table_frame.destroy()
    db_table, db_table_frame = initTable()

def printLabel():
    #TODO
    popup.showwarning(title=None, message="Under development")

def dbTableItemSelected(event):
    #TODO
    #test code, deletes the selected item
    try:
        #get chem ID
        id = db_table.item(db_table.selection())["values"][0]
        chem = readEntry(id)
        id_entry.delete(0, tk.END)
        id_entry.insert(0, chem[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, chem[1])
        cas_entry.delete(0, tk.END)
        cas_entry.insert(0, chem[2])
        formula_entry.delete(0, tk.END)
        formula_entry.insert(0, chem[3])
        qty_entry.delete(0, tk.END)
        qty_entry.insert(0, chem[4])
        purity_entry.delete(0, tk.END)
        purity_entry.insert(0, chem[5])
        supplier_entry.delete(0, tk.END)
        supplier_entry.insert(0, chem[6])
        date_entry.delete(0, tk.END)
        date_entry.insert(0, chem[7])
        mass_entry.delete(0, tk.END)
        mass_entry.insert(0, chem[8])
        mp_entry.delete(0, tk.END)
        mp_entry.insert(0, chem[9])
        bp_entry.delete(0, tk.END)
        bp_entry.insert(0, chem[10])
        density_entry.delete(0, tk.END)
        density_entry.insert(0, chem[11])
        location_entry.delete(0, tk.END)
        location_entry.insert(0, chem[12])
        haz_entry.delete("1.0", tk.END)
        haz_entry.insert("1.0", chem[13])
        prec_entry.delete("1.0", tk.END)
        prec_entry.insert("1.0", chem[14])
        ghs_entry.delete(0, tk.END)
        ghs_entry.insert(0, chem[15])
        misc_entry.delete(0, tk.END)
        misc_entry.insert(0, chem[16])
    except:
        None
    
def editEntryEvent():
    global db_table
    global db_table_frame
    id = db_table.item(db_table.selection())["values"][0]
    selection = db_table.selection()
    editEntry(id,
              chem_name=name_entry.get(),
              chem_cas=cas_entry.get(),
              chem_formula=formula_entry.get(),
              chem_qty=qty_entry.get(),
              chem_purity=purity_entry.get(),
              chem_supplier=supplier_entry.get(),
              chem_date=date_entry.get(),
              chem_mass=mass_entry.get(),
              chem_mp=mp_entry.get(),
              chem_bp=bp_entry.get(),
              chem_density=density_entry.get(),
              chem_location=location_entry.get(),
              chem_haz=haz_entry.get("1.0",'end-1c'),
              chem_prec=prec_entry.get("1.0",'end-1c'),
              chem_ghs=ghs_entry.get(),
              chem_misc=misc_entry.get())
    print("Entry edited.")
    #reload the table
    db_table.destroy()
    db_table_frame.destroy()
    db_table, db_table_frame = initTable()
    db_table.selection_set(selection)
    db_table.focus_set()
    db_table.focus(selection)

def deleteEntryEvent():
    global db_table
    global db_table_frame
    id = db_table.item(db_table.selection())["values"][0]
    deleteEntry(id)
    db_table.destroy()
    db_table_frame.destroy()
    db_table, db_table_frame = initTable()

#initialize the database main window
db_window = tk.Tk()
db_window.title(db_window_title)
db_window.resizable(width=False, height=False)

#initialize database window menu banner
banner_frame = tk.Frame(border=5)
left_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
new_entry_button = tk.Button(text=new_entry_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=newEntryEvent)
new_entry_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
query_button = tk.Button(text=query_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=query)
query_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
refresh_button = tk.Button(text=refresh_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=refresh)
refresh_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
print_label_button = tk.Button(text=print_label_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=printLabel)
print_label_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
delete_entry_button = tk.Button(text=delete_entry_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=deleteEntryEvent)


banner_frame.pack(anchor="w")

def initTable(state:str = None, arg = None):
    """
    state: dictates which type of data has to be displayed. If no value is passed, the entire table is shown.
    """
    #initialize database window table
    db_table_frame = tk.Frame()
    db_table = ttk.Treeview(master=db_table_frame, columns=db_table_headers, show="headings", height=db_table_height)
    for i in enumerate(db_table_headers):
        db_table.heading(db_table_headers[i[0]], text=db_table_header_titles[i[0]])
        db_table.column(db_table_headers[i[0]], width=db_table_column_width[i[0]], stretch=False)
    
    if state == "query": #load query results
        chems = dbQuery(arg)
    else: #load all database entries if nothing is specified
        chems = readEntries()
    for chem, _ in enumerate(chems):
        #the parts of the data to be displayed in the table
        chem_display = chems[chem][0], chems[chem][1], chems[chem][2], chems[chem][4], chems[chem][6], chems[chem][7], chems[chem][12]
        db_table.insert('', tk.END, values=chem_display)

    db_table.bind('<<TreeviewSelect>>', dbTableItemSelected)
    db_table.pack()
    db_table_frame.pack(anchor="nw", side=tk.LEFT)
    return db_table, db_table_frame

#initialize the right display section
right_frame = tk.Frame()

#initialize the label image section
#TODO: Add label design logic
label_frame = tk.Frame(master=right_frame, width=590, height=315, bg="red")
label_spacer = tk.Frame(master=right_frame, height=spacer_dimensions)
info_spacer_left = tk.Frame(master=right_frame, width=spacer_dimensions)

#initialize the info section and frame
info_frame = tk.Frame(master=right_frame)

#Header section
title_frame = tk.Frame(border=5, master=info_frame, background=info_bg)
id_title = tk.Label(text=id_title_name, master=title_frame, background=info_bg)
name_title = tk.Label(text=name_title_name, master=title_frame, background=info_bg)
cas_title = tk.Label(text=cas_title_name, master=title_frame, background=info_bg)
formula_title = tk.Label(text=formula_title_name, master=title_frame, background=info_bg)
qty_title = tk.Label(text=qty_title_name, master=title_frame, background=info_bg)
purity_title = tk.Label(text=purity_title_name, master=title_frame, background=info_bg)
supplier_title = tk.Label(text=supplier_title_name, master=title_frame, background=info_bg)
date_title = tk.Label(text=date_title_name, master=title_frame, background=info_bg)
mass_title = tk.Label(text=mass_title_name, master=title_frame, background=info_bg)
mp_title = tk.Label(text=mp_title_name, master=title_frame, background=info_bg)
bp_title = tk.Label(text=bp_title_name, master=title_frame, background=info_bg)
density_title = tk.Label(text=density_title_name, master=title_frame, background=info_bg)
location_title = tk.Label(text=location_title_name, master=title_frame, background=info_bg)
haz_title = tk.Label(text=haz_title_name, master=title_frame, background=info_bg)
haz_spacer = tk.Frame(master=title_frame, height=info_spacer_height, bg=info_bg)
prec_title = tk.Label(text=prec_title_name, master=title_frame, background=info_bg)
prec_spacer = tk.Frame(master=title_frame, height=info_spacer_height, bg=info_bg)
ghs_title = tk.Label(text=ghs_title_name, master=title_frame, background=info_bg)
misc_title = tk.Label(text=misc_title_name, master=title_frame, background=info_bg)

#field section
entry_frame = tk.Frame(border=5, background=info_bg, master=info_frame)
id_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
name_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
text_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
cas_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
formula_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
qty_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
purity_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
supplier_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
date_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
mass_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
mp_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
bp_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
density_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
location_entry = tk.Entry( master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
haz_entry = tk.Text(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width, height=entry_height)
prec_entry = tk.Text(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width, height=entry_height)
ghs_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)
misc_entry = tk.Entry(master=entry_frame, background=info_bg, font=info_entry_font, width=entry_width)

#initialize the edit entry button
edit_entry_spacer = tk.Frame(master=right_frame, height=5)
edit_entry_button = tk.Button(master=right_frame, background=banner_bg, foreground=banner_fg, text=edit_btn_text, width=83, pady=10, command=editEntryEvent)

#pack database window menu banner
left_spacer.pack(side=tk.LEFT)
new_entry_button.pack(side=tk.LEFT)
new_entry_spacer.pack(side=tk.LEFT)
query_button.pack(side=tk.LEFT)
query_spacer.pack(side=tk.LEFT)
refresh_button.pack(side=tk.LEFT)
refresh_spacer.pack(side=tk.LEFT)
print_label_button.pack(side=tk.LEFT)
print_label_spacer.pack(side=tk.LEFT)
delete_entry_button.pack(side=tk.LEFT)

# initialize the database table and surrounding frame
global db_table
global db_table_frame
try:
    db_table.destroy()
    db_table_frame.destroy()
except:
    None
db_table, db_table_frame = initTable()

#pack right frame
right_frame.pack(side=tk.RIGHT, anchor="se")
info_spacer_left.pack(side=tk.LEFT)

#pack label image section
label_frame.pack(side=tk.TOP, anchor="nw")
label_spacer.pack()
edit_entry_button.pack(side=tk.BOTTOM)
edit_entry_spacer.pack(side=tk.BOTTOM)

#pack info section
info_frame.pack(side=tk.RIGHT, anchor="se")
title_frame.pack(side=tk.LEFT)
id_title.pack(anchor="e")
name_title.pack(anchor="e")
cas_title.pack(anchor="e")
formula_title.pack(anchor="e")
qty_title.pack(anchor="e")
purity_title.pack(anchor="e")
supplier_title.pack(anchor="e")
date_title.pack(anchor="e")
mass_title.pack(anchor="e")
mp_title.pack(anchor="e")
bp_title.pack(anchor="e")
density_title.pack(anchor="e")
location_title.pack(anchor="e")
haz_title.pack(anchor="e")
haz_spacer.pack(anchor="e")
prec_title.pack(anchor="e")
prec_spacer.pack(anchor="e")
ghs_title.pack(anchor="e")
misc_title.pack(anchor="e")

#field section
entry_frame.pack(side=tk.RIGHT)
id_entry.pack()
name_entry.pack()
cas_entry.pack()
formula_entry.pack()
qty_entry.pack()
purity_entry.pack()
supplier_entry.pack()
date_entry.pack()
mass_entry.pack()
mp_entry.pack()
bp_entry.pack()
density_entry.pack()
location_entry.pack()
haz_entry.pack()
prec_entry.pack()
ghs_entry.pack()
misc_entry.pack()

#show the database window
db_window.mainloop()