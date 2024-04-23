import xml.etree.ElementTree as ET
from datetime import datetime
import tkinter.messagebox as popup
import tkinter.simpledialog as dialog

db = "log.xml"
stoich = "stoich.xml"
id_exists_error = f"The ID you are trying to add already exists. ID: "


def addEntry(text: str):
    if text == None or text == "":
        return False
    time = str(datetime.now())[:-7]
    try:
        tree = ET.parse(db)
    except:
        print("No entry found, please open or create a new entry.")
        return False
    tree = ET.parse(db)
    root = tree.getroot()
    print(f"Time: {time}, Text: {text}")
    timestamp = ET.SubElement(root, "timestamp")
    entry_text = ET.SubElement(timestamp, "text")

    timestamp.text = time
    entry_text.text = text
    ET.ElementTree(root).write(db)
    return True

def addStoich(id: str = "-", name: str = "-", M: str = "-", n: str = "-", m: str = "-", V: str = "-", eq: str = "-", notes: str = "-"):
    print("Adding entry")
    try:
        tree = ET.parse(stoich)
    except:
        return None
    root = tree.getroot()
    #check whether the ID already exists
    id_exists = False
    for child in root:
        if child.text == id:
            popup.showerror(message=id_exists_error + str(id)) #temporary
            id_exists = True
            break
    if id_exists == False:
        chem_id = ET.SubElement(root, "chem_id")
        chem_name = ET.SubElement(chem_id, "chem_name")
        chem_M = ET.SubElement(chem_id, "M")
        chem_n = ET.SubElement(chem_id, "n")
        chem_m = ET.SubElement(chem_id, "m")
        chem_V = ET.SubElement(chem_id, "V")
        chem_eq = ET.SubElement(chem_id, "eq")
        chem_notes = ET.SubElement(chem_id, "notes")

        #assignment of values
        chem_id.text = id
        while chem_id.text == "":
            chem_id.text = dialog.askstring("No ID provided.", "Please provide a valid ID:")

        if chem_id.text != "" and chem_id.text != None: #if the user presses cancel, no changes will be saved.
            chem_name.text = name
            chem_M.text = M
            chem_n.text = n
            chem_m.text = m
            chem_V.text = V
            chem_eq.text = eq
            chem_notes.text = notes
            ET.ElementTree(root).write(stoich)
    else:
        raise Exception("The provided ID already exists.")
    return None

def readEntries(): #reads all entries from the database
    try:
        tree = ET.parse(db)
    except:
        return [[None, None]]
    root = tree.getroot()
    data_total = []
    for child in root:
        data = [child.text]
        for grandchild in child:
            data.append(grandchild.text)
        data_total.append(data)
    return data_total

def readStoich():
    print("reading stoich")
    try:
        tree = ET.parse(stoich)
    except:
        return None
    root = tree.getroot()
    data_total = []
    for child in root:
        data = [child.text]
        for grandchild in child:
            data.append(grandchild.text)
        data_total.append(data)
    return data_total
