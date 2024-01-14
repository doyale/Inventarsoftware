import tkinter as tk
from data_management import addEntry
from web import pubChemLookup
import tkinter.simpledialog as dialog

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
edit_btn_text = "Save new entry"
pubchem_btn_text = "Fetch data from PubChem"

info_entry_font = ("Seoge UI", 11)
entry_width = 53
entry_height = 10
info_spacer_height = 153
spacer_dimensions = 18
info_bg = "white"
banner_bg = "light blue"
banner_fg = "black"

def addEntryEvent():
    global id_entry, name_entry, cas_entry, formula_entry, qty_entry, purity_entry, supplier_entry, date_entry, mass_entry, mp_entry, bp_entry, density_entry, location_entry, haz_entry, prec_entry, ghs_entry, misc_entry
    addEntry(id=id_entry.get(),
              name=name_entry.get(),
              cas=cas_entry.get(),
              formula=formula_entry.get(),
              qty=qty_entry.get(),
              purity=purity_entry.get(),
              supplier=supplier_entry.get(),
              date=date_entry.get(),
              mass=mass_entry.get(),
              mp=mp_entry.get(),
              bp=bp_entry.get(),
              density=density_entry.get(),
              location=location_entry.get(),
              haz=haz_entry.get("1.0",'end-1c'),
              prec=prec_entry.get("1.0",'end-1c'),
              ghs=ghs_entry.get(),
              misc=misc_entry.get())
    global window
    window.destroy()

def pubchemFetchEvent():
    global name_entry, cas_entry, formula_entry, mass_entry, mp_entry, bp_entry, density_entry, haz_entry, prec_entry, ghs_entry
    existing_data = [name_entry, cas_entry, formula_entry, mass_entry, mp_entry, bp_entry, density_entry, haz_entry, prec_entry, ghs_entry]
    name, cas, formula, mass, mp, bp, density, ghs, haz, prec = pubChemLookup(dialog.askstring("PubChem lookup", "Please provide a substance name or CAS-number."))
    fetched_data = [name, cas, formula, mass, mp, bp, density, haz, prec, ghs]
    for index, field in enumerate(existing_data):
        if index == 7 or index == 8: #handle haz and prec separately sincce they are text fields and not entry fields
            field.delete("1.0", tk.END)
            field.insert("1.0", fetched_data[index])
        else:
            field.delete(0, tk.END)
            field.insert(0, fetched_data[index])


def newEntry():
    global id_entry, name_entry, cas_entry, formula_entry, qty_entry, purity_entry, supplier_entry, date_entry, mass_entry, mp_entry, bp_entry, density_entry, location_entry, haz_entry, prec_entry, ghs_entry, misc_entry
    #initialize the right display section
    global window
    window = tk.Tk()
    window.attributes("-topmost", True)
    window.update()

    #initialize the info section and frame
    info_frame = tk.Frame(master=window)

    pubchem_fetch_button = tk.Button(master=window, background=banner_bg, foreground=banner_fg, text=pubchem_btn_text, width=83, pady=10,
                                  command=pubchemFetchEvent)

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
    save_entry_spacer = tk.Frame(master=window, height=5)
    save_entry_button = tk.Button(master=window, background=banner_bg, foreground=banner_fg, text=edit_btn_text, width=83, pady=10,
                                  command=addEntryEvent)

    #pack save entry button
    pubchem_fetch_button.pack(side=tk.TOP)
    save_entry_button.pack(side=tk.BOTTOM)
    save_entry_spacer.pack(side=tk.BOTTOM)

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

    window.title("New Entry")

    window.mainloop()