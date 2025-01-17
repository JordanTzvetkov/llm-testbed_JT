import sys
import json
import jsonschema
from utils.handlers import StatusHandler, ConfigHandler
from llms import LLMHandler

def extractGeneIDs(pmid, eraseStatus = False):
    status = StatusHandler(pmid)
    config = ConfigHandler()

    # # Check prerequisites - as we are extracting genes independently we can run in either sequence
    # either species or genes first, then TODO: add a prompt to match them up.
    # if not status.areSpeciesFetched():
    #     return ValueError("Species have not yet been fetched for this paper")

    # Check if already processed
    if eraseStatus:
        print("Erasing existing extractGeneIDs status...")
            # Delete the previous information for extractGeneIDs
        status.updateField("extractGeneIDs", None)
        print("Erased successfully.")
    else:
        if status.areValidGeneIDsExtracted():
            raise ValueError("Genes have already been fetched for this paper")

    # speciesData = status.getSpeciesData()

    # Load paper text
    plaintextFilePath = status.getPlaintextFilePath()
    with open(plaintextFilePath, encoding="utf-8") as plaintextFile:
        paperText = plaintextFile.read()

    # Get system prompt and user prompts from config; use prints to make sure config isn't broken
    systemPrompt = config.getSystemPromptForExtractGeneIDs()
    # print(systemPrompt)
    userPrompts = config.getUserPromptsForExtractGeneIDs()
    # print(userPrompts)
    # for prompt in userPrompts:
    #     print(prompt)
    #     print(f"Prompt Name: {prompt['name']}")
    #     print(f"Prompt Text: {prompt['prompt']}")
    #     print(f"Response Schema: {json.dumps(prompt['responseSchema'], indent=2)}\n")
    # ok these work

    # Initialise LLM with the system prompt
    model = LLMHandler(systemPrompt=systemPrompt)

    # store each prompt result in a dictionary
    extraction_results = {
        "getSymbols": None,
        "getDescriptions": None,
        "getAdditional": None,
        "validateGenes": None
    }

    # Run each step (user prompt) in sequence and collect intermediate results
    # Each user prompt should return a JSON structure with a "genes" field.
    for prompt_config in userPrompts:
        prompt_name = prompt_config["name"]
        prompt_text = prompt_config["prompt"]
        prompt_schema = prompt_config["responseSchema"]

        try:
            # Execute the prompt
            print(f"executing {prompt_name}")
            response = model.askWithRetry(
                f"{prompt_text}\n\nText to analyze: {paperText}",
                textToComplete="{"
            )
            print(f"validating {prompt_name} schema")
            # Validate the response
            prompt_result = json.loads(response)
            jsonschema.validate(prompt_result, schema=prompt_schema)

            # Save valid results
            print(f"extracting {prompt_name} validated results")
            extraction_results[prompt_name] = prompt_result

        except (json.JSONDecodeError, jsonschema.ValidationError) as err:
            # Log individual prompt errors without breaking the loop
            extraction_results[prompt_name] = {"error": str(err)}

        # Update status with results
    try:
        status.updateField("extractGeneIDs", {
            "success": True,
            "results": extraction_results,
            "messageHistory": model.getMessageHistory()
        })
    except Exception as update_err:
        raise Exception(f"Failed to update status: {update_err}")

    return extraction_results

pmid_list =  ['22761895', '8421054', '31289187', '29912472', '21858231'] # ,
              # '1674943', '22379140', '34400833', '33287434', '33997710',
              # '28627360', '33740894', '23418676', '34403450', '25495792',
              # '25017910', '25157665', '30367865', '36624300', '34832608',
              # '22912579', '28205520', '22640832', '29965959', '27551151',
              # '32144363', '35210361', '2007860', '27038925', '34291805',
              # '33214620', '31283102', '25188378', '22174676', '35972967',
              # '28252383', '28202027', '21060817', '29503181', '24586983',
              # '29435408', '23326533', '30794532', '23837822', '27348424',
              # '32184257', '24877144', '27303712', '21282103', '37400439']


for pmid in pmid_list:
    extractGeneIDs(pmid, eraseStatus=True)