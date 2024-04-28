"""
Resources:
https://www.tutorialspoint.com/create-xml-documents-using-python
https://docs.python.org/3/library/xml.etree.elementtree.html
"""

import xml.etree.ElementTree as ET
import tkinter.messagebox as popup
import tkinter.simpledialog as dialog
import os

#Language variables
id_exists_error = f"The ID you are trying to add already exists. ID: "

db = f"{os.path.dirname(os.path.realpath(__file__))}\chem_db.xml"

def editEntry(id, **kwargs):
    tree = ET.parse(db)
    root = tree.getroot()
    chem_id = None
    for chem_id in root.iter("chem_id"):
        if chem_id.text == str(id):
            break
    if chem_id != None:
        for key, value in kwargs.items():
            for i in chem_id.iter(key):
                if i.tag == key:
                    break
            i.text = value
    tree.write(db)

def deleteEntry(id):
    tree = ET.parse(db)
    root = tree.getroot()
   
    chem_id = None
    for chem_id in root.iter("chem_id"):
        if chem_id.text == str(id):
             if popup.askyesno(f"Delete Entry {id}?", f"Do you really want to delete entry {id} ({chem_id[0].text})?") is True:
                print(f"Deleting entry {chem_id.text}.")
                root.remove(chem_id)
                break
             else:
                print(f"Entry {id} not deleted: Canceled by user.")
                break
    tree.write(db)

def readEntries(): #reads all entries from the ddatabase
    try:
        tree = ET.parse(db)
    except:
        return [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
    root = tree.getroot()
    data_total = []
    for child in root:
        data = [child.text]
        for grandchild in child:
            data.append(grandchild.text)
        data_total.append(data)
    return data_total

def readEntry(chem_id: str):
    #Search for a single entry in the chem database.
    entries = readEntries()
    for i, _ in enumerate(entries):
        if str(chem_id) == entries[i][0]:
            data_total = []
            for data, _ in enumerate(entries[i]):
                data_total.append(entries[i][data])
            break #WARNING: WILL ONLY RETURN THE FIRST RESULT; IDS MUST BE UNIQUE!
    return data_total

def addEntry(id, name, cas = "-", formula = "-", qty = "-", purity = "-",
             supplier = "-", date = "-", mass = "-", mp = "-", bp = "-", density = "-",
             location = "-", haz = "-", prec = "-", ghs = "-", misc = "-"):
    # creation of all elements
    try:
        tree = ET.parse(db)
    except:
        root = ET.Element("root")
        ET.ElementTree(root).write(db)
        tree = ET.parse(db)
    root = tree.getroot()

    #check whether the ID already exists
    id_exists = False
    for child in root:
        if child.text == id:
            popup.showerror(message=id_exists_error + str(id)) #temporary
            id_exists = True
            break
    
    if id_exists == False: #If the id is unique, prepare a new entry
        chem_id = ET.SubElement(root, "chem_id")
        chem_name = ET.SubElement(chem_id, "chem_name")
        chem_cas = ET.SubElement(chem_id, "chem_cas")
        chem_formula = ET.SubElement(chem_id, "chem_formula")
        chem_qty = ET.SubElement(chem_id, "chem_qty")
        chem_purity = ET.SubElement(chem_id, "chem_purity")
        chem_supplier = ET.SubElement(chem_id, "chem_supplier")
        chem_date = ET.SubElement(chem_id, "chem_date")
        chem_mass = ET.SubElement(chem_id, "chem_mass")
        chem_mp = ET.SubElement(chem_id, "chem_mp")
        chem_bp = ET.SubElement(chem_id, "chem_bp")
        chem_density = ET.SubElement(chem_id, "chem_density")
        chem_location = ET.SubElement(chem_id, "chem_location")
        chem_haz = ET.SubElement(chem_id, "chem_haz")
        chem_prec = ET.SubElement(chem_id, "chem_prec")
        chem_ghs = ET.SubElement(chem_id, "chem_ghs")
        chem_misc = ET.SubElement(chem_id, "chem_misc")

        #assignment of values
        chem_id.text = id
        while chem_id.text == "":
            chem_id.text = dialog.askstring("No ID provided.", "Please provide a valid ID:")

        if chem_id.text != "" and chem_id.text != None: #if the user presses cancel, no changes will be saved.
            chem_name.text = name
            chem_cas.text = cas
            chem_formula.text = formula
            chem_qty.text = qty
            chem_purity.text = purity
            chem_supplier.text = supplier
            chem_date.text = date
            chem_mass.text = mass
            chem_mp.text = mp
            chem_bp.text = bp
            chem_density.text = density
            chem_location.text = location
            chem_haz.text = haz
            chem_prec.text = prec
            chem_ghs.text = ghs
            chem_misc.text = misc
            #write to XML file
            ET.ElementTree(root).write(db)
            print(f"saved entry {id} to the database.")
    else:
        raise Exception("The provided ID already exists.")

#test code
# teststring = dialog.askstring(title="test", prompt="test chem name:")
# editEntry("65", chem_name=teststring)
# if __name__ == "__main__":
#     deleteEntry(11)
