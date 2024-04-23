import xml.etree.ElementTree as ET
from datetime import datetime

db = "log.xml"

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