import sys
from utils.handlers import StatusHandler, ConfigHandler
import jsonschema
import json
from llms import LLMHandler

def getPaperGenes(pmid):
    status = StatusHandler(pmid)
    config = ConfigHandler()
    
    if not status.areSpeciesFetched():
        return ValueError("Species have not yet been fetched for this paper")
    
    if status.areGenesFetched():
        # TODO: not now, but at some point need to change this so we have a parameter that defines if we skip because
        #  genes are fetched or if we update the current entries in the status.
        return ValueError("Genes have already been fetched for this paper")
    
    speciesData = status.getSpeciesData()

    # TODO: currently we work with one prompt; we want to change the function and config file to allow passing multiple
    # prompts to it; config is sorted, need to update function
    plaintextFilePath = status.getPlaintextFilePath()
    with open(plaintextFilePath, encoding="utf-8") as plaintextFile:
        promptText = plaintextFile.read()
        
    systemPrompt = config.getSystemPromptForGetPaperGenes() + json.dumps(speciesData)
    
    model = LLMHandler(systemPrompt=systemPrompt)

    response = model.askWithRetry(promptText, textToComplete="{")
    
    try:
        fullAnswer = json.loads(response)
        schema = config.getResponseSchemaForGetPaperGenes()
        jsonschema.validate(fullAnswer, schema=schema)
    except Exception as err:
        status.updateField("getPaperGenes", {
            "success": False,
            "error": f"{err}"
        })
        raise Exception(err)
    
    status.updateField("getPaperGenes", {
        "success": True,
        "response": fullAnswer,
        "messageHistory": model.getMessageHistory()
    })
    
    return fullAnswer
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python getPaperGenes.py <pmid>")
        sys.exit(1)
        
    pmid = sys.argv[1]
    
    try:
        genes = getPaperGenes(pmid)
        print(f"Genes for species of paper with PMID {pmid} cached to status file.")
    except Exception as err:
        print(f"Error getting species from paper: {err}")