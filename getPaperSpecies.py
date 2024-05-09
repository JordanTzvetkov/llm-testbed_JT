import sys
from handlers import StatusHandler
from anthropic import Anthropic

def getPaperSpecies(pmid):
    status = StatusHandler(pmid)
    client = Anthropic()
    
    plaintextFilePath = status.getPlaintextFilePath()
    with open(plaintextFilePath) as plaintextFile:
        promptText = plaintextFile.read()
    
    message = client.messages.create(
        max_tokens=1024,
        system="The user will input a series of extracts from a PubMed publication. Respond with only the species that the publication concerns.",
        messages=[
            {
                "role": "user",
                "content": promptText
            }
        ],
        model="claude-3-haiku-20240307",
    )
    
    return message.content[0].text
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python getPaperSpecies.py <pmid>")
        sys.exit(1)
        
    pmid = sys.argv[1]
    
    try:
        species = getPaperSpecies(pmid)
        print(f"Species for paper with PMID {pmid} is: {species}")
    except Exception as err:
        print(f"Error merging sections: {err}")