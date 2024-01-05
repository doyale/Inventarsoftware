"""
Resources:
https://www.tutorialspoint.com/create-xml-documents-using-python
"""

import xml.etree.ElementTree as ET

db = "chem_db.xml"

def editEntry(id, **kwargs):
    tree = ET.parse(db)
    root = tree.getroot()
    chem_id = None
    for chem_id in root.iter("chem_id"):
        if chem_id.text == id:
            break
    if chem_id != None:
        for key, value in kwargs.items():
            for i in chem_id.iter(key):
                if i.tag == key:
                    break
            i.text = value
    tree.write(db)


def addEntry(id, name, cas = None, formula = None, qty = None, purity = None,
             supplier = None, date = None, mass = None, mp = None, bp = None, density = None,
             location = None, haz = None, prec = None, ghs = None, misc = None):
    # creation of all elements
    try:
        tree = ET.parse(db)
    except:
        root = ET.Element("root")
        ET.ElementTree(root).write(db)
    tree = ET.parse(db)
    root = tree.getroot()
    chem_id = ET.SubElement(root, "chem_id")
    #root.append(chem_id)
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

def readEntries():
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

def readEntry(chem_id:str):
    #Search for an entry in the chem database.
    entries = readEntries()
    for i, _ in enumerate(entries):
        if str(chem_id) == entries[i][0]:
            data_total = []
            for data, _ in enumerate(entries[i]):
                data_total.append(entries[i][data])
            break #WARNING: WILL ONLY RETURN THE FIRST RESULT; IDS MUST BE UNIQUE!
    return data_total