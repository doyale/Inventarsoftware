"""
Resources used:
https://realpython.com/python-gui-tkinter/
https://www.pythontutorial.net/tkinter/tkinter-treeview/
"""


import tkinter as tk
import tkinter.messagebox as popup
from tkinter import ttk
import xml.etree.ElementTree as ET
import time

#style variables
banner_height = 2
banner_width = 15
banner_bg = "light blue"
banner_fg = "black"
banner_spacer_width = 3
db_table_column_width = 140
db_table_column_width = (50, 250, 120, 70, 100, 80, 120)

#language specific variables
new_entry_btn_text = "New Entry"
query_btn_text = "Query"
export_btn_text = "Export"
print_label_btn_text = "Print"
db_window_title = "Chemical Database"
db_table_header_titles = ("ID", "Name", "CAS-No.", "Quantity", "Supplier", "Date received", "Storage location")
db_table_headers = ("db_id", "db_name", "db_cas", "db_qty", "db_supplier", "db_date", "db_location")

#other variables

#command functions:
def newEntry():
    #TODO
    #test code
    popup.showwarning(title=None, message="Under development")

def query():
    #TODO
    popup.showwarning(title=None, message="Under development")

def export():
    #TODO
    popup.showwarning(title=None, message="Under development")

def printLabel():
    #TODO
    popup.showwarning(title=None, message="Under development")

def dbTableItemSelected(event):
    #TODO
    #test code, deletes the selected item
    time.sleep(0.05)
    try:
        item = db_table.selection()[0]
        db_table.selection_clear()
        print(item)
        db_table.delete(item)
    except:
        None
    





#initialize the database main window
db_window = tk.Tk()
db_window.title(db_window_title)
db_window.resizable(width=False, height=False)

#initialize database window menu banner
banner_frame = tk.Frame(border=5)
left_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
new_entry_button = tk.Button(text=new_entry_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=newEntry)
new_entry_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
query_button = tk.Button(text=query_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=query)
query_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
export_button = tk.Button(text=export_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=export)
export_spacer = tk.Frame(width=banner_spacer_width, height=banner_height, master=banner_frame)
print_label_button = tk.Button(text=print_label_btn_text, width=banner_width, height=banner_height, bg=banner_bg, fg=banner_fg, master=banner_frame, command=printLabel)
banner_frame.pack(anchor="w")

#initialize database window table
db_table_frame = tk.Frame()
db_table = ttk.Treeview(master=db_table_frame, columns=db_table_headers, show="headings")
for i in enumerate(db_table_headers):
    db_table.heading(db_table_headers[i[0]], text=db_table_header_titles[i[0]])
    db_table.column(db_table_headers[i[0]], width=db_table_column_width[i[0]], stretch=False)
#test data
contacts = []
for n in range(1, 10100, 98):
    contacts.append((f'A {n}', f'Chemical {n}', f'000-{n}-0', f'{n} ml', f'Supplier {n}', f'{n} days ago', f'Cabinet {n}'))
for contact in contacts:
    db_table.insert('', tk.END, values=contact)
db_table.bind('<<TreeviewSelect>>', dbTableItemSelected)
db_table.pack()
db_table_frame.pack(anchor="nw")

#pack database window menu banner
left_spacer.pack(side=tk.LEFT)
new_entry_button.pack(side=tk.LEFT)
new_entry_spacer.pack(side=tk.LEFT)
query_button.pack(side=tk.LEFT)
query_spacer.pack(side=tk.LEFT)
export_button.pack(side=tk.LEFT)
export_spacer.pack(side=tk.LEFT)
print_label_button.pack(side=tk.LEFT)

#show the database window
db_window.mainloop()