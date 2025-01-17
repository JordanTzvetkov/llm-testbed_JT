import os
import json
import utils.helpers as helpers
from . import ConfigHandler
from typing import List

class StatusHandler:
    __status = {}
    
    def __init__(self, pmid: str):
        config = ConfigHandler()
        
        self.__pmid = pmid
        self.__filePath = os.path.join(config.getStatusFolderPath(), f"{self.__pmid}.json")
        
        if os.path.isfile(self.__filePath):
            with open(self.__filePath, "r") as file:
                self.__status = json.load(file)
            
    def get(self):
        return self.__status
    
    def update(self, newStatus):
        self.__status = newStatus
        self.__saveStatus()

    # def updateField(self, field: str | List[str], newValue):
    #     self.__status[field] = newValue if type(field) == str else helpers.traverseDictAndUpdateField(field, newValue, self.__status)
    #     self.__saveStatus()
    def updateField(self, field: str | List[str], newValue):
        """
        Updates the field in the status dictionary. If newValue is None, deletes the field.
        """
        if newValue is None:
            if isinstance(field, str):
                # Log deletion for debugging
                if field in self.__status:
                    print(f"Deleting top-level field: {field}")
                self.__status.pop(field, None)
            else:
                # Log deletion for nested fields
                print(f"Deleting nested field: {field}")
                helpers.traverseDictAndUpdateField(field, None, self.__status, delete=True)
        else:
            if isinstance(field, str):
                self.__status[field] = newValue
            else:
                helpers.traverseDictAndUpdateField(field, newValue, self.__status)

        # Log status after update
        # print(f"Updated status: {self.__status}")

        self.__saveStatus()

    def __saveStatus(self):
        with open(self.__filePath, "w") as file:
            json.dump(self.__status, file, indent=4)
    
    def getStatusFilePath(self):
        return self.__filePath
    
    def getPMID(self):
        return self.__pmid
    
    def getPDFPath(self):
        if not helpers.hasattrdeep(self.__status, ["getPaperPDF", "filename"]):
            raise KeyError("No PDF filename found.")
        
        return os.path.join(ConfigHandler().getPDFsFolderPath(), self.__status['getPaperPDF']['filename'])
    
    def isPDFFetched(self):
        return helpers.hasattrdeep(self.__status, ["getPaperPDF", "success"]) and self.__status["getPaperPDF"]["success"] == True
    
    def isPaperConverted(self):
        return helpers.hasattrdeep(self.__status, ["getPlaintext", "success"]) and self.__status["getPlaintext"]["success"] == True
    
    def getPlaintextFilePath(self):
        if not helpers.hasattrdeep(self.__status, ["getPlaintext", "filename"]):
            raise KeyError("No Plaintext filename found.")
        
        return os.path.join(ConfigHandler().getPlaintextFolderPath(), self.__status['getPlaintext']['filename'])
            
    def isJSONFetched(self):
        return helpers.hasattrdeep(self.__status, ["getPaperJSON", "success"]) and self.__status["getPaperJSON"]["success"] == True
    
    def getJSONFilePath(self):
        if not helpers.hasattrdeep(self.__status, ["getPaperJSON", "filename"]):
            raise KeyError("No JSON filename found.")
        
        return os.path.join(ConfigHandler().getJSONFolderPath(), self.__status['getPaperJSON']['filename'])
    
    def areSpeciesFetched(self):
        return helpers.hasattrdeep(self.__status, ["getPaperSpecies", "success"]) and self.__status["getPaperSpecies"]["success"] == True
    
    def getSpeciesData(self):
        if not self.areSpeciesFetched():
            raise ValueError("Species are not yet fetched for this paper")
        
        return self.__status["getPaperSpecies"]["response"]
    
    def areGenesFetched(self):
        return helpers.hasattrdeep(self.__status, ["getPaperGenes", "success"]) and self.__status["getPaperGenes"]["success"] == True
    
    def getGenesData(self):
        if not self.areGenesFetched():
            raise ValueError("Genes are not yet fetched for this paper")
        
        return self.__status["getPaperGenes"]
    
    def getGeneSpeciesPairs(self):
        if not self.areGenesFetched():
            raise ValueError("Genes are not yet fetched for this paper")
        
        data = self.__status["getPaperGenes"]["response"]
        pairs = [{"species": s["name"], "geneID": g["identifier"]} for s in data["species"] for g in s["genes"]]
        
        seen = []
        for i, pair in enumerate(pairs):
            if pair in seen:
                pairs.pop(i)
            else:
                seen.append(pair)
        
        return pairs
    
    def areGOTermsFetched(self):
        return helpers.hasattrdeep(self.__status, ["getPaperGOTerms", "success"]) and self.__status["getPaperGOTerms"]["success"] == True
    
    def getFetchedGOTerms(self):
        if not self.areGOTermsFetched():
            raise ValueError("Go terms are not yet fetched for this paper")
        
        return self.__status["getPaperGOTerms"]["goTerms"]
    
    def getGeneSpeciesPairsWithFetchedGOTerms(self):
        if not self.areGOTermsFetched():
            raise ValueError("Go terms are not yet fetched for this paper")
        
        return self.__status["getPaperGOTerms"]["geneSpeciesPairsWithGOTerms"]
    
    def areGOTermDescriptionsValidated(self):
        return helpers.hasattrdeep(self.__status, ["validateGOTermDescriptions", "success"]) and self.__status["validateGOTermDescriptions"]["success"] == True
    
    def getAcceptedGOTerms(self):
        if not self.areGOTermDescriptionsValidated():
            raise ValueError("GO term descriptions have not yet been validated for this paper")
        
        return self.__status["validateGOTermDescriptions"]["acceptedGOTerms"]

        #### New Methods for ExtractGeneIDs ####

    def areValidGeneIDsExtracted(self):
        """
        Check if the validateGenes step within extractGeneIDs is marked as successful.
        """
        # Correct key path
        if helpers.hasattrdeep(self.__status, ["extractGeneIDs", "results", "validateGenes"]):
            validate_genes_status = self.__status["extractGeneIDs"]["results"]["validateGenes"]
            # Check if the validateGenes step was successful
            return validate_genes_status.get("success", False)
        return False

    def getExtractedGeneIDsData(self):
        """
        Retrieve validated gene IDs data from extractGeneIDs.
        """
        if not self.areValidGeneIDsExtracted():
            raise ValueError("Gene IDs have not yet been extracted for this paper")
        return self.__status["extractGeneIDs"]["results"]["validateGenes"]["validated_genes"]