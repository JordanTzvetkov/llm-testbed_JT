import sys
import requests
import metapub
from utils.handlers import StatusHandler, ConfigHandler
import os

def getPaperPDF(pmid):
    status = StatusHandler(pmid)
    config = ConfigHandler()
    
    if status.isPDFFetched():
        raise ValueError("Paper already downloaded")
    
    pdfURL = metapub.FindIt(pmid).url
    if pdfURL is None:
        raise ValueError("No PDF found for this paper.")
    
    res = requests.get(pdfURL)
    if res.status_code != 200:
        print(res.reason)
        raise requests.exceptions.RequestException("Failed to fetch PDF")
    
    pdfFileName= f"{pmid}.pdf"
    pdfFilePath = os.path.join(config.getPDFsFolderPath(), pdfFileName)
    
    with open(pdfFilePath, "wb") as pdfFile:
        pdfFile.write(res.content)
        
    status.updateField("getPaperPDF", {
        "success": True,
        "sourceURL": pdfURL,
        "filename": pdfFileName
    })
        
    return pdfFilePath
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python getPaperPDF.py <pmid>")
        sys.exit(1)
        
    pmid = sys.argv[1]
    
    try:
        path = getPaperPDF(pmid)
        print(f"PDF of paper with PMID {pmid} downloaded to {path}")
    except Exception as err:
        print(f"Error downloading paper as PDF: {err}")


getPaperPDF("37939282")