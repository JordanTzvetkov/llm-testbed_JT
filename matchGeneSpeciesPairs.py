import jsonschema
import json
from utils.handlers import StatusHandler, ConfigHandler
from llms import LLMHandler

def matchGeneSpeciesPairs(pmid, eraseStatus=False):
    status = StatusHandler(pmid)
    config = ConfigHandler()

  # Check if already processed
    if status.areValidGeneIDsExtracted():
        if eraseStatus:
            # Delete previous results for matchGeneSpeciesPairs
            status.updateField("matchGeneSpeciesPairs", None)
        else:
            raise ValueError("Gene-species pairs have already been processed for this paper")

    # Get validated genes from the status
    try:
        validated_genes = status.getExtractedGeneIDsData()  # Corrected method usage
        print(validated_genes)
    except KeyError:
        raise ValueError("No validated genes found. Ensure gene extraction has been completed successfully.")




    # Load paper text
    plaintextFilePath = status.getPlaintextFilePath()
    with open(plaintextFilePath, encoding="utf-8") as plaintextFile:
        paperText = plaintextFile.read()
        


    # Get system prompt and user prompts from config
    systemPrompt = config.getSystemPromptForMatchGeneSpeciesPairs()
    userPrompts = config.getUserPromptsForMatchGeneSpeciesPairs()

    # Initialize LLM with the system prompt
    model = LLMHandler(systemPrompt=systemPrompt)

    # Store results dynamically based on prompt names
    results = {}

    # Process each user prompt
    for prompt_config in userPrompts:
        prompt_name = prompt_config["name"]
        prompt_text = prompt_config["prompt"]
        response_schema = prompt_config["responseSchema"]

        # Include validated genes in the prompt context
        enriched_prompt = (
            f"{prompt_text}\n\nText to analyze: {paperText}\n\n"
            f"Validated genes: {json.dumps(validated_genes)}"
        )

        try:
            # Execute the prompt
            response = model.askWithRetry(
                enriched_prompt,
                textToComplete="{"
            )

            # Parse and validate the response
            parsed_response = json.loads(response)
            jsonschema.validate(parsed_response, schema=response_schema)

            # Save valid results
            results[prompt_name] = parsed_response

        except (json.JSONDecodeError, jsonschema.ValidationError) as err:
            # Log individual prompt errors without breaking the loop
            results[prompt_name] = {"error": str(err)}

    # Update status with results
    status.updateField("matchGeneSpeciesPairs", {
        "success": True,
        "results": results,
        "messageHistory": model.getMessageHistory()
    })

    return results
    return results


pmid_list =  ['22761895'] #, '8421054', '31289187', '29912472', '21858231'] # ,
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
    matchGeneSpeciesPairs(pmid, eraseStatus=True)