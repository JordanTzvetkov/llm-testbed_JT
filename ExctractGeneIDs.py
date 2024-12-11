import sys
import json
import jsonschema
from utils.handlers import StatusHandler, ConfigHandler
from llms import LLMHandler


def extractGeneIDs(pmid):
    status = StatusHandler(pmid)
    config = ConfigHandler()

    # # Check prerequisites - as we are extracting genes independently we can run in either sequence
    # either species or genes first, then TODO: add a prompt to match them up.
    # if not status.areSpeciesFetched():
    #     return ValueError("Species have not yet been fetched for this paper")

    # Check if already processed
    # TODO: add re-processing option
    if status.areGenesFetched():
        return ValueError("Genes have already been fetched for this paper")

    speciesData = status.getSpeciesData()

    # Load paper text
    plaintextFilePath = status.getPlaintextFilePath()
    with open(plaintextFilePath, encoding="utf-8") as plaintextFile:
        paperText = plaintextFile.read()

    # Get system prompt and user prompts from config
    systemPrompt = config.getSystemPromptForExtractGeneIDs() + json.dumps(speciesData)
    userPrompts = config.getUserPromptsForExtractGeneIDs()

    # Initialise LLM with the system prompt
    model = LLMHandler(systemPrompt=systemPrompt)

    # Run each step in sequence and collect intermediate results
    # Each user prompt should return a JSON structure with a "genes" field.
    intermediate_results = {}
    for step in userPrompts:
        prompt = step["prompt"]
        response = model.askWithRetry(paperText, textToComplete="{")
        try:
            step_result = json.loads(response)
            # Store the intermediate result keyed by prompt name
            intermediate_results[step["name"]] = step_result
        except Exception as err:
            status.updateField("extractGeneIDs", {
                "success": False,
                "error": f"{err}",
                "promptName": step["name"],
                "response": response
            })
            raise Exception(f"Error parsing response for step {step['name']}: {err}")

    ### TODO: finish script