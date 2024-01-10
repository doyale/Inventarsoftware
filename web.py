import requests
import time

haz_min_percentage = 50 #The minimum percentage of vendors who list a specific hazard statement for the searched chemical.

def pubChemLookup(lookup_name):
    print(f"Looking up {lookup_name} on PubChem...")
    t = time.thread_time()
    ghs = []
    haz = []
    prec = []
    name = None
    mass = None
    mp = None
    bp = None

    attempt = 1
    print(f"Start: {time.thread_time() - t}")
    while True:
        try:
            pug_rest_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/{lookup_name}/cids/json" #PUG REST API URL
            response = requests.get(pug_rest_url)
            cid = response.json()['InformationList']['Information'][0]['CID'][0]
            print(f"CID: {cid}")
            pug_view_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON" #PUG_VIEW API URL
            response = requests.get(pug_view_url)
            name = response.json()["Record"]["RecordTitle"] #Name of the compound according to PubChem
            sections = response.json()["Record"]["Section"]
            break
        except:
            print(f"Could not connect to Pubchem (Attempt {attempt}). Rate limit may be reached or internet may be unstable. Retrying in {attempt*3} seconds...")
            time.sleep(attempt*3)
            attempt += 1
    print(f"Data fetched: {time.thread_time() - t}")


    for item in sections:
        if item["TOCHeading"] == "Safety and Hazards": #Safety section
            safety_section = item
            for hazards in safety_section["Section"][0]['Section'][0]['Information']: #hazards section
                #print(hazards["Name"])
                if hazards["Name"] == "Pictogram(s)": #GHS symbols
                    for symbol in hazards["Value"]['StringWithMarkup'][0]['Markup']:
                        if symbol["Type"] == 'Icon':
                            ghs.append(symbol['Extra'])
                elif hazards["Name"] == "GHS Hazard Statements": #Hazard statements
                    for hazard in hazards["Value"]['StringWithMarkup']:
                        #print(hazard["String"])
                        if hazard["String"][6:8].isdigit(): # will return false if no hazard statements are present
                            if hazard["String"][6:9] == "100" or int(hazard["String"][6:8]) >= haz_min_percentage:
                                haz.append(hazard["String"][0:4])
                        elif hazard["String"][1:3].isdigit() == True: # fallback if no percentage is given
                            haz.append(hazard["String"][0:4])
                elif hazards["Name"] == "Precautionary Statement Codes": #Precautionary statements
                    for precaution in hazards["Value"]['StringWithMarkup'][0]["String"].split(", "):
                        if precaution[:4] == "and ":
                            precaution = precaution[4:]
                        prec.append(precaution)
        elif item["TOCHeading"] == "Chemical and Physical Properties": #Properties section
            properties_section = item["Section"]
            for property in properties_section:
                if property["TOCHeading"] == "Computed Properties":
                    mass = property['Section'][0]['Information'][0]["Value"]["StringWithMarkup"][0]["String"] #molar mass
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
    
    print(f"Done: {time.thread_time() - t}")
    return name, mass, mp, bp, ghs, haz, prec

if __name__ == "__main__":
    lookup_name = input("debug, enter name to search on pubchem: ")
    print(pubChemLookup(lookup_name))
    
