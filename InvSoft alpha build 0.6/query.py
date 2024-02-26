from data_management import readEntries

def dbQuery(input):
    chem_display = []
    chems = readEntries()
    for chem, _ in enumerate(chems): #load the data headers which are to be shown in the table
        for data, _ in enumerate(chems[chem]):
            if chems[chem][data] != None:
                if input in chems[chem][data]:
                    data_tuple = (list(item for item in chems[chem]))
                    chem_display.append(data_tuple)
                    break
    return chem_display

def idQuery(input):
    id_display = []
    chems = readEntries()
    for chem in chems:
        id = chem[0]
        if input in id:
            id_display.append(id)
    return id_display