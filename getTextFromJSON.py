import sys
from utils.handlers import StatusHandler, ConfigHandler
import json
import os

def mergeSections(pmid):
    status = StatusHandler(pmid)
    config = ConfigHandler()
    
    if not status.isJSONFetched():
        raise ValueError("Paper JSON not yet fetched")

    if status.isPaperConverted():
        raise ValueError("Text file already generated")
    
    jsonFilePath = status.getJSONFilePath()
    
    with open(jsonFilePath, "r", encoding="utf-8") as jsonFile:
        article = json.load(jsonFile)
        
    sectionsToGet = config.getMergeSectionsSections()
    sections = {section: "" for section in sectionsToGet}
    
    passages = []
    for a in article:
        for document in a["documents"]:
            passages += document["passages"]
                
    for passage in passages:
        sectionType = passage["infons"]["section_type"].lower()
        if sectionType in sectionsToGet:
            sections[sectionType] = sections[sectionType] + f"{passage['text']}\n"
            
    plaintextFileName = f"{pmid}.txt"
    plaintextFilePath = os.path.join(config.getPlaintextFolderPath(), plaintextFileName)
            
    with open(plaintextFilePath, "w", encoding="utf-8") as plaintextFile:
        for section in sections.values():
            plaintextFile.write(f"{section}\n")
    
    status.updateField("getPlaintext", {
        "success": True,
        "sourceFileType": "json",
        "filename": plaintextFileName
    })
    
    return plaintextFilePath

# pmid_list =  ['22761895', '8421054', '31289187', '29912472', '21858231'] # ,
#               # '1674943', '22379140', '34400833', '33287434', '33997710',
#               # '28627360', '33740894', '23418676', '34403450', '25495792',
#               # '25017910', '25157665', '30367865', '36624300', '34832608',
#               # '22912579', '28205520', '22640832', '29965959', '27551151',
#               # '32144363', '35210361', '2007860', '27038925', '34291805',
#               # '33214620', '31283102', '25188378', '22174676', '35972967',
#               # '28252383', '28202027', '21060817', '29503181', '24586983',
#               # '29435408', '23326533', '30794532', '23837822', '27348424',
#               # '32184257', '24877144', '27303712', '21282103', '37400439']
#
#
# for pmid in pmid_list:
#     mergeSections(pmid)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python getTextFromJSON.py <pmid>")
        sys.exit(1)
        
    pmid = sys.argv[1]
    
    try:
        path = mergeSections(pmid)
        print(f"JSON Paper with PMID {pmid} converted to txt and saved as {path}")
    except Exception as err:
        print(f"Error getting paper from JSON: {err}")