import json 
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConfigHandler:
    def __init__(self, file=str(os.getenv("LLM_TESTBED_CONFIG_PATH"))):
        self.file = file
        with open(file, "r", encoding='utf-8') as f:
            self.__config = json.load(f)
            
    def getConfig(self):
        return self.__config
            
    def refresh(self):
        with open(self.file, "r") as f:
            self.__config = json.load(f)
            
    def getStatusFolderPath(self):
        return self.__config["paths"]["status"]
    
    def getLLMType(self):
        return self.__config["llm"]["current"]["type"]
    
    def getLLM(self):
        return self.__config["llm"]["current"]["model"]
    
    def getPDFsFolderPath(self):
        return self.__config["paths"]["pdf"]
    
    def getPlaintextFolderPath(self):
        return self.__config["paths"]["plaintext"]
    
    def getJSONFolderPath(self):
        return self.__config["paths"]["sections"]
    
    def getMergeSectionsSections(self):
        return self.__config["getTextFromJSON"]["sections"]
    
    # Get Paper Species
    def getSystemPromptForGetPaperSpecies(self):
        return self.__config["getPaperSpecies"]["systemPrompt"]
    
    def getResponseSchemaForGetPaperSepcies(self):
        return self.__config["getPaperSpecies"]["responseSchema"]
    
    # Get Paper Genes
    def getSystemPromptForGetPaperGenes(self):
        return self.__config["getPaperGenes"]["systemPrompt"]
    
    def getResponseSchemaForGetPaperGenes(self):
        return self.__config["getPaperGenes"]["responseSchema"]
    
    # Get Paper GO Terms
    def getSystemPromptStartForGetPaperGOTerms(self):
        return self.__config["getPaperGOTerms"]["systemPromptStart"]
    
    def getResponseSchemaForGetPaperGOTerms(self):
        return self.__config["getPaperGOTerms"]["responseSchema"]
    
    # Validate GO Term Descriptions
    def getSystemPromptStartForValidateGOTermDescriptions(self):
        return self.__config["validateGOTermDescriptions"]["systemPrompt"]
    
    def getResponseSchemaForValidateGOTermDescriptions(self):
        return self.__config["validateGOTermDescriptions"]["responseSchema"]

     #### New Methods for ExtractGeneIDs ####
    # Extract Gene IDs
    def getSystemPromptForExtractGeneIDs(self):
        return self.__config["extractGeneIDs"]["systemPrompt"]

    # def getResponseSchemaForExtractGeneIDs(self):    # not needed, changed so schema is provided for each prompt
    #     return self.__config["extractGeneIDs"]["responseSchema"]

    def getUserPromptsForExtractGeneIDs(self):
        return self.__config["extractGeneIDs"]["userPrompts"]

    def getResponseSchemaForPrompt(self, prompt_name):
        """
        Retrieve the response schema for a specific user prompt by name.
        :param prompt_name: Name of the user prompt (e.g., 'getSymbols', 'getDescriptions').
        :return: The response schema of the specified prompt.
        """
        prompts = self.__config["extractGeneIDs"]["userPrompts"]
        for prompt in prompts:
            if prompt["name"] == prompt_name:
                    return prompt["responseSchema"]
        raise KeyError(f"Prompt '{prompt_name}' not found in extractGeneIDs configuration.")

    # Match Gene Species Pairs
    def getSystemPromptForMatchGeneSpeciesPairs(self):
        return self.__config["matchGeneSpeciesPairs"]["systemPrompt"]

    def getUserPromptsForMatchGeneSpeciesPairs(self):
        return self.__config["matchGeneSpeciesPairs"]["userPrompts"]

    def getResponseSchemaForPrompt(self, prompt_name):
        """
        Retrieve the response schema for a specific user prompt by name.
        :param prompt_name: Name of the user prompt (e.g., 'initialAssignment', 'validateAssignments').
        :return: The response schema of the specified prompt.
        """
        prompts = self.__config["matchGeneSpeciesPairs"]["userPrompts"]
        for prompt in prompts:
            if prompt["name"] == prompt_name:
                return prompt["responseSchema"]
        raise KeyError(f"Prompt '{prompt_name}' not found in matchGeneSpeciesPairs configuration.")