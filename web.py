import requests
import time

haz_min_percentage = 50 #The minimum percentage of vendors who list a specific hazard statement for the searched chemical.

def pubChemLookup(lookup_name):
    print(f"Looking up {lookup_name} on PubChem...")
    ghs = []
    haz = []
    prec = []
    name = None
    mass = None

    attempt = 1
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
            properties_section = item
            mass = properties_section["Section"][0]['Section'][0]['Information'][0]["Value"]["StringWithMarkup"][0]["String"] #molar mass
        
    return name, mass, ghs, haz, prec

lookup_name = "palladium chloride"
print(pubChemLookup(lookup_name))