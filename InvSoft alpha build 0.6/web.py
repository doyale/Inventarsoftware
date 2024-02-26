import subprocess
import sys
try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
import time
import tkinter.messagebox as popup

haz_min_percentage = 50 #The minimum percentage of vendors who list a specific hazard statement for the searched chemical.

def pubChemLookup(lookup_name):
    print(f"Looking up {lookup_name} on PubChem...")
    t = time.thread_time()
    ghs = []
    haz = []
    prec = []
    name = ""
    formula = ""
    cas = ""
    mass = ""
    mp = ""
    bp = ""
    density = ""

    print(f"Start: {time.thread_time() - t}")
    try:
        pug_rest_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/{lookup_name}/cids/json" #PUG REST API URL
        response = requests.get(pug_rest_url)
        cid = response.json()['InformationList']['Information'][0]['CID'][0]
        print(f"CID: {cid}")
        pug_view_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON" #PUG_VIEW API URL
        response = requests.get(pug_view_url)
        name = response.json()["Record"]["RecordTitle"] #Name of the compound according to PubChem
        sections = response.json()["Record"]["Section"]
    except:
        popup.showerror("Error", "Could not fetch data from PubChem. Please try again.")
        return name, mass, mp, bp, density, ghs, haz, prec
    print(f"Data fetched: {time.thread_time() - t}")


    for item in sections:
        if item["TOCHeading"] == "Safety and Hazards": #Safety section
            safety_section = item
            for hazards in safety_section["Section"][0]['Section'][0]['Information']: #hazards section
                #print(hazards["Name"])
                if hazards["Name"] == "Pictogram(s)": #GHS symbols
                    for symbol in hazards["Value"]['StringWithMarkup'][0]['Markup']:
                        if symbol["Type"] == 'Icon':
                            match symbol['Extra']:
                                case "Explosive":
                                    if "GHS01" not in ghs:
                                        ghs.append("GHS01")
                                case "Flammable":
                                    if "GHS02" not in ghs:
                                        ghs.append("GHS02")
                                case "Oxidizer":
                                    if "GHS03" not in ghs:
                                        ghs.append("GHS03")
                                case "Compressed Gas":
                                    if "GHS04" not in ghs:
                                        ghs.append("GHS04")
                                case "Corrosive":
                                    if "GHS05" not in ghs:
                                        ghs.append("GHS05")
                                case "Acute Toxic":
                                    if "GHS06" not in ghs:
                                        ghs.append("GHS06")
                                case "Irritant":
                                    if "GHS07" not in ghs:
                                        ghs.append("GHS07")
                                case "Health Hazard":
                                    if "GHS08" not in ghs:
                                        ghs.append("GHS08")
                                case "Environmental Hazard":
                                    if "GHS09" not in ghs:
                                        ghs.append("GHS09")
                                case other:
                                    None
                elif hazards["Name"] == "GHS Hazard Statements": #Hazard statements
                    for hazard in hazards["Value"]['StringWithMarkup']:
                        #print(hazard["String"])
                        if hazard["String"][6:8].isdigit(): # will return false if no hazard statements are present
                            if hazard["String"][6:9] == "100" or int(hazard["String"][6:8]) >= haz_min_percentage:
                                if hazard["String"][0:4] not in haz:
                                    haz.append(hazard["String"][0:4])
                        elif hazard["String"][1:3].isdigit() == True: # fallback if no percentage is given
                            if hazard["String"][0:4] not in haz:
                                haz.append(hazard["String"][0:4])
                elif hazards["Name"] == "Precautionary Statement Codes": #Precautionary statements
                    for precaution in hazards["Value"]['StringWithMarkup'][0]["String"].split(", "):
                        if precaution[:4] == "and ":
                            precaution = precaution[4:]
                        if precaution not in prec:
                            prec.append(precaution)
        elif item["TOCHeading"] == "Chemical and Physical Properties": #Properties section
            properties_section = item["Section"]
            for property in properties_section:
                if property["TOCHeading"] == "Computed Properties":
                    mass = property['Section'][0]['Information'][0]["Value"]["StringWithMarkup"][0]["String"] + " g/mol" #molar mass
                elif property["TOCHeading"] == "Experimental Properties":
                    for exp in property['Section']:
                        try:
                            if exp["TOCHeading"] == "Melting Point": #Melting point
                                for melting_point in exp["Information"]:
                                    if "StringWithMarkup" in melting_point["Value"]:
                                        if melting_point["Value"]["StringWithMarkup"][0]["String"][-1:] == "C":
                                            mp = melting_point["Value"]["StringWithMarkup"][0]["String"]
                        except:
                            print("Melting point could not be fetched.")
                        try:
                            if exp["TOCHeading"] == "Boiling Point": #Boiling point
                                for boiling_point in exp["Information"]:
                                    if "StringWithMarkup" in boiling_point["Value"]:
                                        if boiling_point["Value"]["StringWithMarkup"][0]["String"][-1:] == "C":
                                            bp = boiling_point["Value"]["StringWithMarkup"][0]["String"]
                        except:
                            print("Boiling point could not be fetched.")

                        if exp["TOCHeading"] == "Density": #Density
                            for dens in exp["Information"]:
                                if "StringWithMarkup" in dens["Value"]:
                                    dens_string = dens["Value"]["StringWithMarkup"][0]["String"]
                                    # Reads the density string until no more digits appear, then uses the most precise value.
                                    dens_temporary = dens_string[:2] #Initial two characters are always present so no need to check for digits here.
                                    char_digit = 2
                                    while len(dens_string) >= char_digit + 1 and dens_string[char_digit].isdigit() == True:
                                        dens_temporary = dens_temporary + dens_string[char_digit]
                                        char_digit += 1
                                    if len(density) < len(dens_temporary):
                                        density = dens_temporary
                            if density != "":
                                density = density + " g/ml"
        elif item["TOCHeading"] == "Names and Identifiers":
            for identifier in item["Section"]:
                if identifier["TOCHeading"] == "Molecular Formula": #molecular formula section
                    formula = identifier["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

                elif identifier["TOCHeading"] == "Other Identifiers":
                    for sub_identifier in identifier["Section"]:
                        if sub_identifier["TOCHeading"] == "CAS": #CAS section
                            cas = sub_identifier["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

                

    print(f"Done: {time.thread_time() - t}")
    #processing code here:
    # haz = hazmatCondenser(haz)
    # prec = precautionaryCondenser(haz, prec)

    return name, cas, formula, mass, mp, bp, density, ghs, haz, prec


if __name__ == "__main__":
    lookup_name = input("debug, enter name to search on pubchem: ")
    print(pubChemLookup(lookup_name))