import requests
import json

def pubChemLookup(lookup_name):
    ghs = []
    pug_rest_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/{lookup_name}/cids/json" #PUG REST API URL
    response = requests.get(pug_rest_url)
    cid = response.json()['InformationList']['Information'][0]['CID'][0]
    pug_view_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON" #PUG_VIEW API URL
    response = requests.get(pug_view_url)
    sections = response.json()["Record"]["Section"]
    for item in sections:
    #    print(data["Record"]["Section"][item]["TOCHeading"])
        if item["TOCHeading"] == "Safety and Hazards":
            safety_section = item
            for hazards in safety_section["Section"][0]['Section'][0]['Information']: #hazards section
                try:
                    for symbol in hazards["Value"]['StringWithMarkup'][0]['Markup']:
                        if symbol["Type"] == 'Icon':
                            ghs.append(symbol['Extra'])
                except:
                    None
    return ghs

lookup_name = "10294-64-1"
print(pubChemLookup(lookup_name))