

import sys
from utils.handlers import StatusHandler, ConfigHandler
import json
import requests
import os


def getPaperJSON(pmid: str):
    status = StatusHandler(pmid)
    config = ConfigHandler()

    if status.isJSONFetched():
        raise ValueError("Paper JSON already fetched")

    url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmid}/unicode"

    # Try fetching JSON data
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch JSON for PMID {pmid}: {e}")
        return None  # Return None or handle as needed

    # Attempt to parse JSON data
    try:
        articleJSON = json.loads(res.content)
    except json.JSONDecodeError:
        print(f"Invalid JSON response for PMID {pmid}")
        return None

    # Write JSON data to file
    jsonFileName = f"{pmid}.json"
    jsonFilePath = os.path.join(config.getJSONFolderPath(), jsonFileName)

    try:
        with open(jsonFilePath, "w", encoding="utf-8") as sectionsFile:
            json.dump(articleJSON, sectionsFile, indent=4)
    except IOError as e:
        print(f"Failed to save JSON for PMID {pmid} to {jsonFilePath}: {e}")
        return None

    # Update status
    status.updateField("getPaperJSON", {
        "success": True,
        "sourceURL": url,
        "filename": jsonFileName
    })

    return jsonFilePath


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python getPaperJSON.py <pmid>")
        sys.exit(1)

    pmid = sys.argv[1]

    # Try calling getPaperJSON with error handling
    try:
        path = getPaperJSON(pmid)
        if path:
            print(f"JSON file of paper with PMID {pmid} downloaded to {path}")
        else:
            print(f"Error: JSON file for PMID {pmid} could not be downloaded.")
    except Exception as err:
        print(f"Error getting paper as JSON: {err}")




































# import sys
# from utils.handlers import StatusHandler, ConfigHandler
# import json
# import requests
# import os
# from bs4 import BeautifulSoup
#
#
# def fetch_PMID_related_data(pmid: str):
#     url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch PubMed page for PMID {pmid}: {e}")
#         return None, None  # Return None if page fetch fails
#
#     # Parse the page content
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Attempt to extract DOI
#     doi_element = soup.find('a', {'class': 'id-link', 'data-ga-category': 'full_text', 'data-ga-action': 'DOI'})
#     doi = doi_element['href'].replace('https://doi.org/', '') if doi_element else None
#
#     # Attempt to extract PMC ID
#     pmc_element = soup.find('a', {'class': 'id-link', 'data-ga-category': 'full_text', 'data-ga-action': 'PMCID'})
#     pmc_id = pmc_element.text.strip() if pmc_element else None
#
#     return doi, pmc_id
#
#
# def fetch_JSON_via_PMC(pmc_id: str):
#     pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmc_id}&format=json&tool=pmc_json_retriever&email=jt1995@liverpool.ac.uk"
#     try:
#         response = requests.get(pmc_url)
#         response.raise_for_status()
#         articleJSON = json.loads(response.content)
#         print(f"Successfully fetched JSON via PMC for PMC ID {pmc_id}")
#         return articleJSON
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch JSON via PMC for PMC ID {pmc_id}: {e}")
#     except json.JSONDecodeError:
#         print(f"Invalid JSON response for PMC ID {pmc_id}")
#     return None
#
#
#
# def getPaperJSON(pmid: str):
#     status = StatusHandler(pmid)
#     config = ConfigHandler()
#
#     if status.isJSONFetched():
#         raise ValueError("Paper JSON already fetched")
#
#     url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmid}/unicode"
#
#     # Try fetching JSON data
#     try:
#         res = requests.get(url)
#         res.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
#         articleJSON = json.loads(res.content)
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch JSON for PMID {pmid}: {e}")
#         articleJSON = None  # Proceed even if JSON fetching fails
#     except json.JSONDecodeError:
#         print(f"Invalid JSON response for PMID {pmid}")
#         articleJSON = None
#
#     # Fetch DOI and PMC ID
#     # print(f"Attempting to fetch DOI and PMC for {pmid}")
#     # doi, pmc_id = fetch_DOI_and_PMC(pmid)
#
#     # If JSON fetch failed, try fetching JSON via PMC ID if available
#     # if articleJSON is None and pmc_id:
#     #     print(f"Attempting to fetch JSON using PMC ID {pmc_id}")
#     #     articleJSON = fetch_JSON_via_PMC(pmc_id)
#
#     # Write JSON data to file if available
#     if articleJSON is not None:
#         jsonFileName = f"{pmid}.json"
#         jsonFilePath = os.path.join(config.getJSONFolderPath(), jsonFileName)
#
#         try:
#             with open(jsonFilePath, "w", encoding="utf-8") as sectionsFile:
#                 json.dump(articleJSON, sectionsFile, indent=4)
#         except IOError as e:
#             print(f"Failed to save JSON for PMID {pmid} to {jsonFilePath}: {e}")
#             return None
#
#     # Update status with JSON status, DOI, and PMC ID
#     status.updateField("getPaperJSON", {
#         "success": articleJSON is not None,
#         "sourceURL": url,
#         "filename": jsonFileName if articleJSON is not None else None,
#         "doi": doi,
#         "pmc_id": pmc_id
#     })
#
#     return jsonFilePath if articleJSON is not None else None
#
#
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python getPaperJSON.py <pmid>")
#         sys.exit(1)
#
#     pmid = sys.argv[1]
#
#     # Try calling getPaperJSON with error handling
#     try:
#         path = getPaperJSON(pmid)
#         if path:
#             print(f"JSON file of paper with PMID {pmid} downloaded to {path}")
#         else:
#             print(f"Error: JSON file for PMID {pmid} could not be downloaded.")
#     except Exception as err:
#         print(f"Error getting paper as JSON: {err}")

# import sys
# from utils.handlers import StatusHandler, ConfigHandler
# import json
# import requests
# import os
# from bs4 import BeautifulSoup # for web scraping where pmid fails
#
#
# def fetch_DOI_and_PMC(pmid: str):
#     url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch PubMed page for PMID {pmid}: {e}")
#         return None, None  # Return None if page fetch fails
#
#     # Parse the page content
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Attempt to extract DOI
#     doi_element = soup.find('a', {'class': 'id-link', 'data-ga-category': 'full_text', 'data-ga-action': 'DOI'})
#     doi = doi_element['href'].replace('https://doi.org/', '') if doi_element else None
#
#     # Attempt to extract PMC ID
#     pmc_element = soup.find('a', {'class': 'id-link', 'data-ga-category': 'full_text', 'data-ga-action': 'PMCID'})
#     pmc_id = pmc_element.text.strip() if pmc_element else None
#
#     return doi, pmc_id
#
# def getPaperJSON(pmid: str):
#     status = StatusHandler(pmid)
#     config = ConfigHandler()
#
#     if status.isJSONFetched():
#         raise ValueError("Paper JSON already fetched")
#
#     url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmid}/unicode"
#
#     # Try fetching JSON data
#     try:
#         res = requests.get(url)
#         res.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch JSON for PMID {pmid}: {e}")
#         return None  # Return None or handle as needed
#
#     # Attempt to parse JSON data
#     try:
#         articleJSON = json.loads(res.content)
#     except json.JSONDecodeError:
#         print(f"Invalid JSON response for PMID {pmid}")
#
#         # Fallback to fetch DOI and PMC ID
#         doi, pmc_id = fetch_DOI_and_PMC(pmid)
#         if doi or pmc_id:
#             print(f"DOI: {doi if doi else 'Not available'}, PMC ID: {pmc_id if pmc_id else 'Not available'}")
#         else:
#             print("DOI and PMC ID could not be retrieved.")
#         return None
#
#
#
#         return None
#
#     # Write JSON data to file
#     jsonFileName = f"{pmid}.json"
#     jsonFilePath = os.path.join(config.getJSONFolderPath(), jsonFileName)
#
#     try:
#         with open(jsonFilePath, "w", encoding="utf-8") as sectionsFile:
#             json.dump(articleJSON, sectionsFile, indent=4)
#     except IOError as e:
#         print(f"Failed to save JSON for PMID {pmid} to {jsonFilePath}: {e}")
#         return None
#
#     # Update status
#     status.updateField("getPaperJSON", {
#         "success": True,
#         "sourceURL": url,
#         "filename": jsonFileName
#     })
#
#     return jsonFilePath
#
#
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python getPaperJSON.py <pmid>")
#         sys.exit(1)
#
#     pmid = sys.argv[1]
#
#     # Try calling getPaperJSON with error handling
#     try:
#         path = getPaperJSON(pmid)
#         if path:
#             print(f"JSON file of paper with PMID {pmid} downloaded to {path}")
#         else:
#             print(f"Error: JSON file for PMID {pmid} could not be downloaded.")
#     except Exception as err:
#         print(f"Error getting paper as JSON: {err}")